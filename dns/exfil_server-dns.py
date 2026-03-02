#!/usr/bin/env python3
import hashlib
from logging import log
import os
import argparse
import time
from dnslib import QTYPE, RCODE
from dnslib.server import DNSServer, BaseResolver, DNSLogger

LOG_DIR = "captures"

os.makedirs(LOG_DIR, exist_ok=True)

class AuditResolver(BaseResolver):

    def resolve(self, request, handler):
        reply = request.reply()

        original_qname = str(request.q.qname).strip(".")
        qname_lower = original_qname.lower()

        qtype = QTYPE[request.q.qtype]
        src_ip, src_port = handler.client_address
        ts = time.strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{ts}] {src_ip}:{src_port} -> {qtype} {original_qname}")

        if not qname_lower.endswith("." + dns_host):
            reply.header.rcode = RCODE.NOERROR
            return reply

        prefix_length = len("." + dns_host)
        prefix = original_qname[:-prefix_length]

        if not prefix:
            reply.header.rcode = RCODE.NOERROR
            return reply

        parts = prefix.split(".")

        if len(parts) < 2:
            reply.header.rcode = RCODE.NOERROR
            return reply

        identificador_original = parts[-1]
        identificador_hash = identificador_original.lower()

        payload_parts = parts[:-1]

        payload_original = "".join(payload_parts)

        if payload_original:

            md5_name = hashlib.md5(
                identificador_hash.encode()
            ).hexdigest()

            filepath = os.path.join(LOG_DIR, md5_name)

            with open(filepath, "a") as f:
                f.write(payload_original+"\n")

        reply.header.rcode = RCODE.NOERROR
        return reply


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic python server built to receive data over DNS queries.",epilog="""Created by: Xen00rw""")
    parser.add_argument("--dns-host", action="store", type=str, required=True, dest='host', help='Host to bind DNS server to')
    args = parser.parse_args()
    dns_host = args.host.lower()
    resolver = AuditResolver()
    logger = DNSLogger(prefix=False)
    

    print("* DNS Host should be subdomain.test.com")
    print("* DNS Queries should be in the format: <payload>.<identifier 000 to yyy>.subdomain.test.com")
    print("* We recomend using hexadecimal for dump, since DNS is case-insensitive.")
    print("Example: 000000000000000.abc.subdomain.test.com")

    udp_server = DNSServer(resolver, port=53, address="0.0.0.0", logger=logger)
    tcp_server = DNSServer(resolver, port=53, address="0.0.0.0", tcp=True, logger=logger)

    udp_server.start_thread()
    tcp_server.start_thread()

    print(f"DNS audit collector running on 0.0.0.0:53")

    while True:
        time.sleep(3600)