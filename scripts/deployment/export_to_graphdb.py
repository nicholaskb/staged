#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List, Optional, Tuple


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload TTL files to GraphDB (RDF4J HTTP API).")
    default_url = os.getenv("GRAPHDB_URL", "http://localhost:7200")
    default_repo = os.getenv("GRAPHDB_REPOSITORY")
    default_context = os.getenv("GRAPHDB_CONTEXT")
    default_user = os.getenv("GRAPHDB_USER")
    default_pass = os.getenv("GRAPHDB_PASSWORD")

    default_files = [
        str(Path("/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_base.ttl")),
        str(Path("/Users/nicholasbaro/Python/staged/output/current/cmc_stagegate_instances.ttl")),
    ]

    parser.add_argument("--graphdb-url", default=default_url, help="GraphDB base URL (default from GRAPHDB_URL).")
    parser.add_argument("--repository", default=default_repo, required=default_repo is None, help="Repository ID (GRAPHDB_REPOSITORY).")
    parser.add_argument("--context", default=default_context, help="Named graph IRI for upload (GRAPHDB_CONTEXT).")
    parser.add_argument("--user", default=default_user, help="Basic auth user (GRAPHDB_USER).")
    parser.add_argument("--password", default=default_pass, help="Basic auth password (GRAPHDB_PASSWORD).")
    parser.add_argument("--files", nargs="+", default=default_files, help="TTL files to upload (order preserved).")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Print actions without sending requests.")
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Actually send requests.")
    parser.set_defaults(dry_run=True)
    parser.add_argument("--max-retries", type=int, default=5, help="Max retries for 429/5xx responses (default: 5)")
    parser.add_argument("--timeout", type=float, default=60.0, help="HTTP timeout seconds (default: 60)")
    return parser.parse_args(argv)


def build_endpoint(base_url: str, repository: str, context_iri: Optional[str]) -> str:
    base = base_url.rstrip("/") + f"/repositories/{urllib.parse.quote(repository)}/statements"
    if not context_iri:
        return base
    # RDF4J expects context parameter as an encoded IRI in angle brackets
    ctx = context_iri.strip()
    if not (ctx.startswith("<") and ctx.endswith(">")):
        ctx = f"<{ctx}>"
    q = urllib.parse.urlencode({"context": ctx})
    return f"{base}?{q}"


def detect_content_type(path: Path) -> str:
    if path.suffix.lower() in {".ttl", ".turtle"}:
        return "text/turtle"
    if path.suffix.lower() in {".nt"}:
        return "application/n-triples"
    if path.suffix.lower() in {".rdf", ".xml"}:
        return "application/rdf+xml"
    return "text/plain"


def build_auth_header(user: Optional[str], password: Optional[str]) -> Optional[str]:
    if not user or password is None:
        return None
    token = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def upload_file(
    file_path: Path,
    endpoint: str,
    content_type: str,
    auth_header: Optional[str],
    timeout: float,
    max_retries: int,
) -> Tuple[bool, int, str]:
    data = file_path.read_bytes()
    attempt = 0
    backoff = 1.0

    while True:
        attempt += 1
        req = urllib.request.Request(endpoint, data=data, method="POST")
        req.add_header("Content-Type", content_type)
        req.add_header("Content-Length", str(len(data)))
        if auth_header:
            req.add_header("Authorization", auth_header)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.getcode()
                return True, status, "OK"
        except urllib.error.HTTPError as e:
            status = e.code
            # Retry on 429 and 5xx
            if status == 429 or 500 <= status < 600:
                if attempt >= max_retries:
                    return False, status, f"HTTPError after {attempt} attempts: {e.reason}"
                time.sleep(backoff)
                backoff = min(backoff * 2, 30.0)
                continue
            return False, status, f"HTTPError: {e.reason}"
        except Exception as e:
            if attempt >= max_retries:
                return False, -1, f"Error after {attempt} attempts: {e}"
            time.sleep(backoff)
            backoff = min(backoff * 2, 30.0)
            continue


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    endpoint = build_endpoint(args.graphdb_url, args.repository, args.context)
    auth_header = build_auth_header(args.user, args.password)

    print(f"Target endpoint: {endpoint}")
    if args.dry_run:
        print("Mode: DRY RUN (no data will be sent)")

    for f in args.files:
        p = Path(f).resolve()
        if not p.exists():
            print(f"Skip missing file: {p}")
            continue
        ctype = detect_content_type(p)
        size = p.stat().st_size
        print(f"Upload: {p.name} ({size} bytes) as {ctype}")
        if args.dry_run:
            continue
        ok, status, msg = upload_file(p, endpoint, ctype, auth_header, args.timeout, args.max_retries)
        if ok:
            print(f"  -> Success (HTTP {status})")
        else:
            print(f"  -> Failed (HTTP {status}): {msg}")
            return 1

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

