#!/usr/bin/env python3
"""
房源记录管理脚本 - house-hunter skill

功能：
  - 新增房源记录
  - 列出所有已记录房源
  - 更新房源状态（待看 / 已看 / 已排除 / 心仪）
  - 删除房源记录
  - 导出房源为 CSV 或 Markdown

用法：
  python save_listings.py add --title "房源名称" --price 8000 --area 太阳宫 --type 整租 --rooms 2室1厅 --floor 5/18 --direction 南 --subway 10分钟 --url "链接" --notes "备注"
  python save_listings.py list [--status 待看]
  python save_listings.py update --id 1 --status 已看 --notes "采光很好"
  python save_listings.py delete --id 1
  python save_listings.py export [--format csv|markdown] [--output 文件路径]
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path


# 存储路径：用户主目录下的 .house-hunter 文件夹
STORAGE_DIR = Path.home() / ".house-hunter"
STORAGE_FILE = STORAGE_DIR / "listings.json"

STATUS_OPTIONS = ["待看", "已看", "心仪", "已排除"]


def ensure_storage():
    """确保存储目录和文件存在"""
    STORAGE_DIR.mkdir(exist_ok=True)
    if not STORAGE_FILE.exists():
        STORAGE_FILE.write_text(json.dumps([], ensure_ascii=False, indent=2), encoding="utf-8")


def load_listings():
    ensure_storage()
    return json.loads(STORAGE_FILE.read_text(encoding="utf-8"))


def save_listings(listings):
    STORAGE_FILE.write_text(json.dumps(listings, ensure_ascii=False, indent=2), encoding="utf-8")


def next_id(listings):
    if not listings:
        return 1
    return max(l["id"] for l in listings) + 1


def cmd_add(args):
    listings = load_listings()
    record = {
        "id": next_id(listings),
        "title": args.title,
        "price": args.price,
        "area": args.area or "",
        "type": args.type or "",
        "rooms": args.rooms or "",
        "floor": args.floor or "",
        "direction": args.direction or "",
        "subway": args.subway or "",
        "url": args.url or "",
        "notes": args.notes or "",
        "status": "待看",
        "added_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    listings.append(record)
    save_listings(listings)
    print(f"✅ 已添加房源 [ID:{record['id']}]：{record['title']}  {record['price']}元/月")


def cmd_list(args):
    listings = load_listings()
    if args.status:
        listings = [l for l in listings if l["status"] == args.status]
    if not listings:
        print("暂无符合条件的房源记录。")
        return
    print(f"\n{'ID':<4} {'状态':<6} {'标题':<22} {'价格':>7} {'区域':<8} {'房型':<8} {'朝向':<4} {'地铁':<8} {'添加日期'}")
    print("-" * 90)
    for l in listings:
        print(f"{l['id']:<4} {l['status']:<6} {l['title']:<22} {str(l['price'])+'元':<7} "
              f"{l['area']:<8} {l['rooms']:<8} {l['direction']:<4} {l['subway']:<8} {l['added_at']}")
    print()


def cmd_update(args):
    listings = load_listings()
    for l in listings:
        if l["id"] == args.id:
            if args.status:
                if args.status not in STATUS_OPTIONS:
                    print(f"❌ 状态不合法，可选值：{', '.join(STATUS_OPTIONS)}")
                    return
                l["status"] = args.status
            if args.notes is not None:
                l["notes"] = args.notes
            if args.price is not None:
                l["price"] = args.price
            l["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_listings(listings)
            print(f"✅ 已更新房源 [ID:{args.id}]")
            return
    print(f"❌ 未找到 ID 为 {args.id} 的房源")


def cmd_delete(args):
    listings = load_listings()
    new_listings = [l for l in listings if l["id"] != args.id]
    if len(new_listings) == len(listings):
        print(f"❌ 未找到 ID 为 {args.id} 的房源")
        return
    save_listings(new_listings)
    print(f"✅ 已删除房源 [ID:{args.id}]")


def cmd_export(args):
    listings = load_listings()
    if not listings:
        print("暂无房源记录可导出。")
        return

    fmt = args.format or "markdown"
    output = args.output

    if fmt == "csv":
        output = output or str(STORAGE_DIR / "listings.csv")
        fields = ["id", "title", "price", "area", "type", "rooms", "floor",
                  "direction", "subway", "status", "notes", "url", "added_at"]
        with open(output, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(listings)
        print(f"✅ 已导出 CSV：{output}")

    else:  # markdown
        output = output or str(STORAGE_DIR / "listings.md")
        lines = ["# 房源记录\n", f"导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n",
                 "| ID | 状态 | 标题 | 价格 | 区域 | 房型 | 朝向 | 地铁距离 | 添加日期 | 备注 |",
                 "|---|---|---|---|---|---|---|---|---|---|"]
        for l in listings:
            lines.append(
                f"| {l['id']} | {l['status']} | [{l['title']}]({l.get('url','')}) | "
                f"{l['price']}元/月 | {l['area']} | {l['rooms']} | {l['direction']} | "
                f"{l['subway']} | {l['added_at']} | {l.get('notes','')} |"
            )
        with open(output, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"✅ 已导出 Markdown：{output}")


def main():
    parser = argparse.ArgumentParser(description="房源记录管理工具")
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="新增房源")
    p_add.add_argument("--title", required=True, help="房源标题")
    p_add.add_argument("--price", type=int, required=True, help="月租金（元）")
    p_add.add_argument("--area", help="所在区域")
    p_add.add_argument("--type", help="租型（整租/合租）")
    p_add.add_argument("--rooms", help="户型（如2室1厅）")
    p_add.add_argument("--floor", help="楼层（如5/18）")
    p_add.add_argument("--direction", help="朝向（南/北/东/西）")
    p_add.add_argument("--subway", help="距地铁距离（如10分钟）")
    p_add.add_argument("--url", help="房源链接")
    p_add.add_argument("--notes", help="备注")

    # list
    p_list = sub.add_parser("list", help="列出房源")
    p_list.add_argument("--status", choices=STATUS_OPTIONS, help="按状态筛选")

    # update
    p_update = sub.add_parser("update", help="更新房源")
    p_update.add_argument("--id", type=int, required=True, help="房源ID")
    p_update.add_argument("--status", choices=STATUS_OPTIONS, help="新状态")
    p_update.add_argument("--notes", help="新备注")
    p_update.add_argument("--price", type=int, help="新价格")

    # delete
    p_delete = sub.add_parser("delete", help="删除房源")
    p_delete.add_argument("--id", type=int, required=True, help="房源ID")

    # export
    p_export = sub.add_parser("export", help="导出房源")
    p_export.add_argument("--format", choices=["csv", "markdown"], default="markdown", help="导出格式")
    p_export.add_argument("--output", help="输出文件路径")

    args = parser.parse_args()

    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "update": cmd_update,
        "delete": cmd_delete,
        "export": cmd_export,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
