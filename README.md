# Once said

一個能夠隨機讀取頻道內訊息並回傳的機器人。附贈氣象預報功能。

## 設定
### setting.json
- [token]用你的token取代。如何獲得可參考[這篇](https://navoni1024.github.io/Discord-Bot-create-a-bot/)
- prefix: 可以換成你想要的字元或字串
- photoLimit: 一串輸出裡面最多可以出現的相片數
- mlimit: 使用`m`指令時最多的輸出行數

### blacklist.json
在裡面填寫不想被機器人偵測的頻道。格式 "頻道名":ID

## 執行
安裝requirement.txt的套件，接著執行
```python
python3 main.py
```

## 功能

- 標機器人或使用prefix召喚機器人: 隨機輸出一行
- 標機器人或使用prefix召喚機器人+ m + 數字:  隨機輸出m行，預設4行，最高`mlimit`行`
- 標機器人或使用prefix召喚機器人+ w + 縣市名: 天氣預報
