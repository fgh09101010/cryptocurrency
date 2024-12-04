import get
import sql


if __name__ == "__main__":
    for id,coin in sql.get_name():
        data = get.get_history(coin)
        if data is None:
            print(f"無法抓取 {coin} 的歷史數據，跳過此幣。")
            continue
        for item in data:
            sql.save_data(id, item)

