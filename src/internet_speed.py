import speedtest

# returns the user download speed
def download_speed():

    retry = 0
    speed = False
    while speed == False and retry < 4:

        try:

            speed_test = speedtest.Speedtest()

            download_speed = speed_test.download()

            mbps = download_speed / (1024 * 1024)

            speed = True

        except:

            mbps = "Error"

            retry += 1

    return mbps


# returns the waiting time
def delay(mbps):

    if mbps <= 10:

        x = 30

    elif mbps <= 25:

        x = 20

    elif mbps <= 75:

        x = 15

    else:

        x = 10

    return x


# returns the average time it takes to download a pdf file taken as a 5 point moving average
# def delay(end_time, start_time, download_time_list):

# max_waiting_time = 30

# waiting_time = random.randrange(10, 15, 1)

# download_time = end_time - start_time

# download_time_list.append(download_time)

# if len(download_time_list) != 1:

#     prev_wait = download_time_list[-2]

# else:

#     prev_wait = 0

# if len(download_time_list) < 6:

#     avg_download_time = (
#         ((waiting_time + sum(download_time_list)) / len(download_time_list))
#         - prev_wait
#     ) * 2

# else:

#     avg_download_time = ((sum(download_time_list[-5:]) / 5) - prev_wait) * 2

# if avg_download_time <= max_waiting_time:

#     print(avg_download_time)
#     return avg_download_time

# else:

#     print(max_waiting_time)
#     return max_waiting_time
