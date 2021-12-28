import os
import string
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

SRC_PATH = Path(".").resolve().parent
DJANGO_DB_PATH = SRC_PATH / "python/db.sqlite3"


def run(cwd, cmd, **kwargs):
    print(f"{cwd}$", *cmd)
    process = subprocess.run(cmd, check=False, cwd=cwd, **kwargs)
    rc = process.returncode
    if rc != 0:
        sys.exit(rc)


def rsync(src, url, *, excludes=None):
    src = str(src) + "/"
    cmd = ["rsync", "--recursive", "--itemize-changes"]
    if excludes:
        cmd.extend(["--exclude-from", excludes])
    cmd.extend([src, url])
    run(Path.cwd(), cmd)


def ssh(url, cmd):
    cmd = ["ssh", url, cmd]
    run(Path.cwd(), cmd)


def scp(src, url):
    cmd = ["scp", src, url]
    run(Path.cwd(), cmd)


def generate_from_template(in_path, gen_path, letter):
    in_text = in_path.read_text()
    out_text = in_text.replace("@letter@", letter)
    gen_path.mkdir(exist_ok=True)
    out_path = gen_path / f"{letter}.conf"
    out_path.write_text(out_text)
    print("Generated", out_path)


def generate_nginx_server_conf(c):
    in_path = SRC_PATH / "infra/nginx/servers/sub.conf.in"
    gen_path = SRC_PATH / "infra/nginx/servers/gen/"
    generate_from_template(in_path, gen_path, c)

    in_path = SRC_PATH / "infra/nginx/upstreams/conf.in"
    gen_path = SRC_PATH / "infra/nginx/upstreams/gen/"
    generate_from_template(in_path, gen_path, c)


def deploy_nginx(args):
    for c in string.ascii_lowercase:
        generate_nginx_server_conf(c)
    src = SRC_PATH / "infra/nginx"
    rsync(src, "root@hr.dmerej.info:/etc/nginx")
    ssh("root@hr.dmerej.info", "nginx -t")
    ssh("root@hr.dmerej.info", "nginx -s reload")


def deploy_backend(args):
    src = SRC_PATH / "python"
    excludes_file = src / ".rsyncexcludes"
    rsync(src, "hr@hr.dmerej.info:src/kata-hr-manager/python", excludes=excludes_file)
    to_restart = [f"gunicorn@{c}.service" for c in string.ascii_lowercase]
    ssh("root@hr.dmerej.info", f"systemctl restart {' '.join(to_restart)}")


def migrate_django_db():
    cwd = SRC_PATH / "python"
    DJANGO_DB_PATH.unlink(missing_ok=True)
    cmd = ["poetry", "run", "python", "manage.py", "migrate"]
    run(cwd, cmd)


def re_init_remote_dbs():
    # Copy the newly migrated db
    scp(DJANGO_DB_PATH, "hr@hr.dmerej.info:/srv/hr/data/init.db")

    # Copy the script and run it
    local_script = SRC_PATH / "infra/re-init-dbs.sh"
    remote_script = "/srv/hr/data/re-init-dbs.sh"
    scp(local_script, f"hr@hr.dmerej.info:{remote_script}")
    ssh("hr@hr.dmerej.info", remote_script)


def reset_dbs(args):
    migrate_django_db()
    re_init_remote_dbs()


def main():
    parser = ArgumentParser()
    actions = parser.add_subparsers(help="available actions", dest="action")

    deploy_backend_parser = actions.add_parser("deploy-backend")
    deploy_backend_parser.set_defaults(action=deploy_backend)

    deploy_nginx_parser = actions.add_parser("deploy-nginx")
    deploy_nginx_parser.set_defaults(action=deploy_nginx)

    reset_db_parser = actions.add_parser("reset-dbs")
    reset_db_parser.set_defaults(action=reset_dbs)

    args = parser.parse_args()
    if not args.action:
        parser.print_help()
        sys.exit(2)

    args.action(args)


if __name__ == "__main__":
    main()
