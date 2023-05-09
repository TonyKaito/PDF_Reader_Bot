import json


def read_file(file_path):
  with open(file_path, 'r') as file:
    # Reading from json file
    json_dict = json.load(file)
    return json_dict


def update_file(json_dict, file_path):
  with open(file_path, 'w') as file:
    # Writing into json file
    json.dump(json_dict, file)


def add_new_server(json_dict, guildID, channelID):
  json_dict[str(guildID)] = {
    "channelID": channelID,
    "PgPerLoop": 2,
    "LoopInterval": 60, # default value in minutes
    "BookQueue": []
  }

  update_file(json_dict, './data.json')

  
def add_book(json_dict, url_to_pdf, guildID, page_count, title, author=""):
  json_dict[str(guildID)]["BookQueue"].append([url_to_pdf, title, author, 0, page_count])

  update_file(json_dict, './data.json')


def del_cur_book(json_dict, guildID):
  del json_dict[str(guildID)]["BookQueue"][0]

  update_file(json_dict, './data.json')

def set_channel(json_dict, guildID, channelID):
  json_dict[str(guildID)]["channelID"] = channelID

  update_file(json_dict, './data.json')

def get_page(json_dict, guildID):
  return json_dict[str(guildID)]["BookQueue"][0][0]


def get_page_no(json_dict, guildID):
  return json_dict[str(guildID)]["BookQueue"][0][3]


def get_page_total(json_dict, guildID):
  return json_dict[str(guildID)]["BookQueue"][0][4]


def get_page_info(json_dict, guildID):
  return json_dict[str(guildID)]["BookQueue"][0][1:4]


def get_interval(json_dict, guildID):
  return json_dict[str(guildID)]["LoopInterval"]


def next_page(json_dict, guildID):
  json_dict[str(guildID)]["BookQueue"][0][3] += 1

  update_file(json_dict, './data.json')


def get_book_list(json_dict, guildID):
  size = len(json_dict[str(guildID)]["BookQueue"])
  book_list = []
  for i in range(0, size):
    book_list.append(json_dict[str(guildID)]["BookQueue"][i][1:5])
    
  return book_list


def set_interval(json_dict, guildID, interval):
  json_dict[str(guildID)]["LoopInterval"] = interval

  update_file(json_dict, './data.json')


def set_per_loop(json_dict, guildID, perloop):
  json_dict[str(guildID)]["PgPerLoop"] = perloop

  update_file(json_dict, './data.json')
