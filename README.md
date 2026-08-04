# nonebot-plugin-tutu

从 yppp.net 获取随机二次元图片，支持多张合并发送。

## 功能

- 发送随机二次元图片（横图/竖图/随机）
- 支持数量参数，上限 15 张
- 多张图片合并为一条消息发送
- 本地缓存 URL，减少 API 调用
- 分批发送，内存友好

## 安装

```bash
pip install nonebot-plugin-tutu
```

## 配置

在 NoneBot2 的 `.env` 或 `.env.prod` 中添加以下配置项：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `tutu_max_count` | int | 15 | 单次最大数量 |
| `tutu_default_count` | int | 1 | 默认数量 |
| `tutu_orientation` | str | `random` | 方向偏好：`random`（随机）、`pc`（横屏）、`pe`（竖屏） |
| `tutu_api_timeout` | int | 10 | 请求超时（秒） |
| `tutu_headers_json` | str | `{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Accept": "application/json"}` | 自定义请求头（JSON 字符串） |

配置示例（`config`）：

```dotenv
tutu_max_count=15
tutu_default_count=1
```

## 使用

命令格式：

示例：
- `/图图` → 发送 1 张
- `/图图 3` → 发送 3 张（同一条消息）

## 数据源

默认使用 [yppp.net](https://api.yppp.net/)

- 横图接口：`pc.php?return=all`
- 竖图接口：`pe.php?return=all`
tutu_api_timeout=10
tutu_headers_json={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
