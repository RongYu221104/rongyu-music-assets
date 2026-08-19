# RongYu 音乐背景资料库

这是一组与馆藏音频并行保存的中文背景资料。它不代替唱片原始内页，也不把传闻写成史实；能够落到录音日期、地点、人员或音乐家自述的内容，均在文末留有来源。

## 馆藏范围

- 5 位核心音乐家：Bill Evans、Miles Davis、Dave Brubeck、Paul Desmond、Jim Hall
- 6 张专辑：*From Left to Right*、*Kind of Blue*、*Time Out*、*Undercurrent*、*Waltz for Debby*、*You Must Believe in Spring*
- 32 首曲目：与 `../audio/` 当前馆藏逐一对应

## 阅读入口

- [音乐家](artists.md)：生平、音乐性格与照片
- [专辑](albums.md)：录音现场、幕后故事与创作语境
- [曲目](tracks.md)：逐曲署名、来历、馆藏版本的演奏时间与地点
- [来源与图片授权](sources.md)：核验链接、访问日期、作者及许可
- [机器可读索引](catalog.json)：供网站或其他工具读取的路径与覆盖统计
- [版本化背景资料接口](api/v1/context.json)：播放器与背景资料板使用的完整 JSON 数据

## 编辑原则

1. “录制于”只描述馆藏所采用的唱片版本；一首标准曲的初演、首录与本馆版本不是同一件事。
2. 没有可靠的一手自述时，不替音乐家虚构“创作心境”。此类条目会明确写成“未查到可核验自述”。
3. 作曲、作词与演奏分别署名。*Blue in Green* 的历史署名争议亦如实保留。
4. 人物照片和插图只采用公有领域、明确开放许可或“无已知出版限制”的馆藏图，并在 `sources.md` 逐张记录。
5. 本批资料核验日期为 2026-08-19。网页可能迁移，永久馆藏链接优先。

## 接口约定

`api/v1/context.json` 是静态、跨页面可缓存的只读接口，包含 `artists`、`albums`、`tracks` 三组实体。每个实体都有稳定 `id`、正文段落、元数据、图片及来源入口；网站只保存这些稳定 ID，不复制背景正文。

修改 Markdown 后运行 `python scripts/build_music_context_api.py`，生成文件中的覆盖数必须保持为 5 位音乐家、6 张专辑和 32 首曲目。
