import os
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

SRC_PATH = Path(".").resolve().parent
DJANGO_DB_PATH = SRC_PATH / "backend/db.sqlite3"

def get_teams(num_teams):
    return list("abcdefghijklmnopqrstuvwxyz")[0:num_teams]

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


def scp_multi(sources, url):
    cmd = ["scp", *sources, url]
    run(Path.cwd(), cmd)


def generate_from_template(in_path, gen_path, group, team):
    in_text = in_path.read_text()
    out_text = in_text.replace("@group@", group).replace("@team@", team)
    gen_parent_path = gen_path.parent
    gen_parent_path.mkdir(exist_ok=True, parents=True)
    gen_path.write_text(out_text)
    print("Generated", gen_path)


def generate_nginx_server_conf(group, team):
    in_path = SRC_PATH / "infra/nginx/servers/sub.conf.in"
    gen_path = SRC_PATH / f"infra/nginx/servers/gen/{group}-{team}.conf"
    generate_from_template(in_path, gen_path, group, team)

    in_path = SRC_PATH / "infra/nginx/upstreams/conf.in"
    gen_path = SRC_PATH / f"infra/nginx/upstreams/gen/{group}-{team}.conf"
    generate_from_template(in_path, gen_path, group, team)


def deploy_nginx(args):
    group = args.group
    for team in get_teams(args.num_teams):
        generate_nginx_server_conf(group, team)
    src = SRC_PATH / "infra/nginx"
    rsync(src, "root@hr.dmerej.info:/etc/nginx")
    ssh("root@hr.dmerej.info", "nginx -t")
    ssh("root@hr.dmerej.info", "nginx -s reload")


def deploy_backend(args):
    src = SRC_PATH / "backend"
    excludes_file = src / ".rsyncexcludes"
    group = args.group
    rsync(src, f"hr@hr.dmerej.info:src/{group}", excludes=excludes_file)

    if args.restart:
        restart_backend(args)


def restart_backend(args):
    group = args.group
    teams = get_teams(args.num_teams)
    to_restart = [f"gunicorn-{group}-{team}.socket" for team in teams]
    ssh("root@hr.dmerej.info", f"systemctl restart {' '.join(to_restart)}")


def migrate_django_db():
    cwd = SRC_PATH / "backend"
    DJANGO_DB_PATH.unlink(missing_ok=True)
    cmd = ["poetry", "run", "python", "manage.py", "migrate"]
    run(cwd, cmd)


def re_init_remote_dbs(args):
    group = args.group
    scp(DJANGO_DB_PATH, "hr@hr.dmerej.info:/srv/hr/data/init.db")
    for team in get_teams(args.num_teams):
        ssh("hr@hr.dmerej.info", f"cp /srv/hr/data/init.db /srv/hr/data/{group}/{team}.db")


def reset_dbs(args):
    migrate_django_db()
    re_init_remote_dbs(args)


def deploy_systemd(args):
    group = args.group
    to_copy = []
    for team in get_teams(args.num_teams):
        src_path = SRC_PATH / "infra/systemd/gunicorn.in.socket"
        gen_path = SRC_PATH / f"infra/systemd/gen/gunicorn-{group}-{team}.socket"
        generate_from_template(src_path, gen_path, group, team)
        to_copy.append(gen_path)

        src_path = SRC_PATH / "infra/systemd/gunicorn.in.service"
        gen_path = SRC_PATH / f"infra/systemd/gen/gunicorn-{group}-{team}.service"
        generate_from_template(src_path, gen_path, group, team)
        to_copy.append(gen_path)

    dest_path = f"root@hr.dmerej.info:/etc/systemd/system"
    scp_multi(to_copy, dest_path)

    ssh("root@hr.dmerej.info", "systemctl daemon-reload")
    restart_backend(args)


def main():
    parser = ArgumentParser()
    parser.add_argument("--group", required=True)
    parser.add_argument("--num-teams", required=True, type=int)
    actions = parser.add_subparsers(help="available actions", dest="action", required=True)

    deploy_backend_parser = actions.add_parser("deploy-backend")
    deploy_backend_parser.add_argument("--no-restart", action="store_false", dest="restart")
    deploy_backend_parser.set_defaults(action=deploy_backend, restart=True)

    deploy_systemd_parser = actions.add_parser("deploy-systemd")
    deploy_systemd_parser.set_defaults(action=deploy_systemd)

    deploy_nginx_parser = actions.add_parser("deploy-nginx")
    deploy_nginx_parser.set_defaults(action=deploy_nginx)

    reset_db_parser = actions.add_parser("reset-dbs")
    reset_db_parser.set_defaults(action=reset_dbs)

    restart_backend_parsed = actions.add_parser("restart-backend")
    restart_backend_parsed.set_defaults(action=restart_backend)

    args = parser.parse_args()

    args.action(args)


if __name__ == "__main__":
    main()
