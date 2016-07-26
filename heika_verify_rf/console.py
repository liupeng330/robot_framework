from libs.model.verify_third_party_mock import JuxinliIdCard
from libs.model.verify_third_party_mock import JuxinliMobile

if __name__ == "__main__":
    juxinli_id_card = JuxinliIdCard('110108198403300031')
    # juxinli_id_card.write_hit_black_list_response()
    # juxinli_id_card.write_not_hit_black_list_response()
    juxinli_id_card.write_not_hit_black_list_response()

    juxinli_cell_phone = JuxinliMobile('13520207836')
    # juxinli_cell_phone.write_hit_black_list_response()
    # juxinli_cell_phone.write_not_hit_black_list_response()
    juxinli_cell_phone.write_query_error_black_list_response()
