# AzurLaneScripts
基于cv图像匹配的碧蓝航线自动刷图脚本
使用方法：
1.安装adb和依赖
2.手机打开usb调试和adb


3.数据线连接pc
4.打开游戏进入到章节选关界面
5.启动脚本
python AzurLaneAuto.py


注意事项：
1.请务必保证S通关
2.去除所有潜艇编队
3.未考虑的情况：
	（1）船舱已满
	（2）捞到紫或金船，需要多点一下
	（3）道路不通
需要手动处理，方法是当脚本输出判断战斗状态时，手动进入到战斗状态即可继续自动执行
4.目前仅支持3-4，其他图的方法：
	（1）截图关卡的名称（见/resource/image/3-4.png），格式.png，放到/resource/image下
	（2）修改AzurLaneAuto.py中的stage变量为你的图片后缀前的名称
	（3）进入到对应章节选关界面，启动脚本