import get
import sql


if __name__ == "__main__":
    for id,coin in sql.get_name():
        skip_list=["USDT"]
        if coin in skip_list:
            continue
        for data in get.get_history(coin):
            sql.save_data(id,data)

