
def filter_cnts_basedOn_num(contours , num):
    return  [cnt for cnt in contours if ( len(cnt)==num)]