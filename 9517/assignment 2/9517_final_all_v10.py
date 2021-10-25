import os
from scipy.spatial.distance import cdist
import cv2 as cv
import numpy as np
from scipy import signal
from scipy import ndimage as ndi
from skimage.segmentation import watershed
import matplotlib.pyplot as plt

name_dataset_1 = 'DIC-C2DH-HeLa-2'
name_dataset_2 = 'Fluo-N2DL-HeLa'
name_dataset_3 = 'PhC-C2DL-PSC'
name_dataset_4 = 'DIC-C2DH-HeLa'

name_dataset = [name_dataset_1,name_dataset_2,name_dataset_3,name_dataset_4]
track_open=False    #是否打开框选模式（如果打开就手动更改为True）
blur_size=10     # 面积和的模糊值（原细胞面积-模糊值<两个细胞的面积和<原细胞面积+模糊值，并且距离不能大于原始细胞直径）
smllest_cell_area=10    # 判断为是细胞的最小面积
biggest_diff=30    #两个细胞的最大差距，如果比这个还大就说明没找到对应的细胞
data_num = 1  # insert the dataset number
sequence_num = 0

def read_img_name():   #read the file
    name = {}
    tif_name = {}
    for dataset_name in name_dataset:
        key = dataset_name
        name[key] = []
        file_name_all = os.listdir(dataset_name)
        file_name_all.sort()
        for file_name in file_name_all:
            if 'Masks' in file_name:
                continue
            else:
                name[key].append(dataset_name+'/'+file_name)
        for item in name[key]:
            key_f = item
            tif_name[key_f] = []
            for file_name in os.listdir(item):
                tif_name[key_f].append(item+'/'+file_name)
    return name,tif_name

def normalize(image):     #normalize the image in 0~255
    img = image.copy().astype(np.float32)
    img -= img.min()
    img = np.clip(img, 0, 180) #improve the light 提高亮度，方便处理
    img /= img.max()
    img *= 255
    return img.astype(np.uint8)

def normalize_after(image):   #ignore the light , normal normalize
    img = image.copy().astype(np.float32)
    img -= img.min()
    img /= img.max()
    img *= 255
    return img.astype(np.uint8)


def water_box(w_la,image):  #use to draw the box in the orignal image
    img = cv.cvtColor(image, cv.COLOR_GRAY2BGR) #change the grey image to the color image
    n = 0
    centers_radiu = []  # 储存细胞质心和半径
    countours = []
    for i in range(1,np.array(w_la).max()):
        np_arr = np.array(w_la)
        np_arr[np.where(np_arr != i)] = 0 #set other pixel to zero
        #获取每一个细胞的轮廓
        #cv.imshow("test", np_arr.astype(np.uint8))
        #cv.waitKey(0)
        #cv.destroyWindow("test")

        contours, hierarchy = cv.findContours(np_arr.astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv.contourArea(cnt)  #get the area of the cnt
            if area < smllest_cell_area:     #delete the wrong noisy cnt
                continue
            else:
                (x, y), radius = cv.minEnclosingCircle(cnt)
                radius = int(radius)
                #min_rect = cv.minAreaRect(cnt)  # get min_area_rectangle
                #min_rect = np.int0(cv.boxPoints(min_rect))
                centers_radiu.append([int(x), int(y), radius, n])
                #cv.drawContours(img, [min_rect], 0, (82, 122, 247), thickness=1) #draw the min_area_rectangle
                x1, y1, w, h = cv.boundingRect(cnt)
                rect_pic = cv.rectangle(img, (x1, y1), (x1 + w, y1 + h), (221, 160, 221), 1)
                countours.append(cnt)
                n += 1

    cv.putText(img , f"The number of cells is: {len(centers_radiu)}", (10, 50), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 0),1)
    return img , centers_radiu,countours


def segment(image,data_name):

    img_f = normalize(image) #normalize and light the image

    if data_name == 2:
        img_f = cv.blur(img_f, (7, 7))

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  #set kernel size

    Open = cv.morphologyEx(img_f, cv.MORPH_OPEN, kernel, iterations=3) #use morphology open function to delete some noise

    iterations_set = [(50, 50), (9, 9)]   #the different value for different set

    erode = cv.erode(Open, kernel, iterations=iterations_set[data_name - 2][0])
    dilate = cv.dilate(erode, kernel, iterations=iterations_set[data_name - 2][1])

    img = img_f - dilate  # delete the background light

    img = normalize_after(img) #use the normal version to nomalize image

    thresh_type = [cv.THRESH_BINARY, cv.THRESH_BINARY + cv.THRESH_OTSU]

    thresh_value = [20,0]

    _, thresh = cv.threshold(img, thresh_value[data_name - 2], 255, thresh_type[data_name - 2]) # get the cells

    iterations_erode = [6, 2]

    sure_bg = cv.dilate(thresh, kernel, iterations=1)  # the sure backgound

    sure_fg = cv.erode(thresh, kernel, iterations=iterations_erode[data_name - 2]) #get the sure cell part
    '''

    peak , centers_radiu ,cell_num= center(sure_fg) #use the sure cell part to get the center of the cell
    '''

    img_array = np.array(thresh) #get the mask

    dist_transform = cv.distanceTransform(sure_bg, cv.DIST_L2, 0) #caculate the distance

    markers = ndi.label(sure_fg)[0] #create markers label

    labels = watershed(-dist_transform, markers, mask=img_array) #use watershed to seperate cells

    labels = labels.astype(np.uint8)

    output ,countours, bboxes = water_box(labels, img_f) #draw the box of the cell

    return output,output,countours,bboxes


def segment_1(img,norimg):
    #gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    (_, thresh) = cv.threshold(img, 250, 255, cv.THRESH_BINARY)
    #cv.imshow("thresh", thresh)
    #cv.waitKey(0)
    #cv.destroyWindow("test")
    _,contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # 转rgb，因为画的框是rgb的
    norimg = cv.cvtColor(norimg, cv.COLOR_GRAY2BGR)
    centers_radiu = []  # 储存细胞质心和半径
    cell_radius = 4  # 最小细胞半径
    n = 0
    for cnt in contours:
        try:
            # 获取能包裹细胞的最小圆形的半径和中心
            # print("cnt",cnt)
            (x, y), radius = cv.minEnclosingCircle(cnt)
            radius = int(radius)
            #cv.circle(norimg, (int(x),int(y)), radius,(221, 160, 221),2,0)

            # print(x,y,radius)
            # 判断是否属于细胞
            if radius > cell_radius:
                # 获取质心
                # print(x,y)
                centers_radiu.append([int(x), int(y), radius, n])
                x1, y1, w, h = cv.boundingRect(cnt)  # 绘制矩形外框
                # 对normalize的图片标注
                rect_pic = cv.rectangle(norimg, (x1, y1), (x1 + w, y1 + h), (221, 160, 221), 1)
        except ZeroDivisionError:
            pass
        n += 1

    cell_num = len(centers_radiu)
    cv.putText(rect_pic, f"The number of cells is: {cell_num}", (10, 50), cv.FONT_HERSHEY_COMPLEX, 0.5, (100, 200, 200),
                1)
    """cv2.imshow("rect_pic",rect_pic)
    cv2.waitKey(0)"""

    return norimg,centers_radiu, contours



def main():

    name, path_tif = read_img_name()
    key = name[name_dataset[data_num - 1]][sequence_num]
    key_0 = name[name_dataset[-1]][sequence_num]
    print(key)  # print the file name
    list_a = path_tif[key]  # get all the image_name
    list_a.sort()
    length = len(list_a)  # the number if image
    sequence_tif = []  # 存这个文件夹下所有图片的像素内容

    list_a_0 = path_tif[key_0]
    list_a_0.sort()

    sequence_0 = [] # 存原图
    for i in range(length) :
        img_f = cv.imread(list_a[i], cv.IMREAD_GRAYSCALE)
        #cv.imshow('tif',img_f)
        sequence_tif.append(img_f)
        if data_num == 1:
            img_0 = cv.imread(list_a_0[i], cv.IMREAD_GRAYSCALE)
            #cv.imshow('tif_0', img_0)
            sequence_0.append(img_0)
    # 图片处理
    last_img_center=[] #保存上一张图片上所有细胞的位置和半径
    line_dict={} #保存每次轨迹的线（的两个点）
    clear_time=30 # 每10次开始覆盖之前的线
    cell_id_dict={} #给每个细胞一个id，存储他们的中点
    id=0
    n=1
    for i_img in range(length):
        tmp_list=[] #存储这张图上的所有轨迹
        img=sequence_tif[i_img]
        devid=0 #正在分裂的细胞计数
        if data_num == 1:
            original_img = sequence_0[i_img]

            #norming为原始图片对应的正则化后的图，所以应该还有个读原始图和找原始图对应图的步骤
            norimg= normalize(original_img)
            norimg,centers_radiu, contours = segment_1(img,norimg)
        else:
            norimg,img , centers_radiu , contours = segment(img, data_num)
        # detect返回一个细胞点列表和半径列表，去下一张图的时候寻找中点最近的和半径最接近的（相加取最小）

        if last_img_center != []:
            # 如果有上一帧
            for k in range(len(last_img_center)):
                # 先遍历每一个前一帧细胞
                diff_cen = {}
                all_diff={}
                last_center = last_img_center[k]
                l_x = last_center[0]
                l_y = last_center[1]
                l_r = last_center[2]
                for i in range(len(centers_radiu)):
                    # 遍历每一个细胞中点，去找坐标最相近的点
                    x=centers_radiu[i][0]
                    y=centers_radiu[i][1]
                    radius=centers_radiu[i][2]

                    # 中点距离差权重为0.7， 半径差权重为0.3
                    both_diff = 0.7 * (ed(np.array([x, y]), np.array([l_x, l_y])) + 0.3 * (abs(radius - l_r)))
                    center_diff = ed(np.array([x, y]), np.array([l_x, l_y]))
                    diff_cen[i]=center_diff
                    all_diff[i]=both_diff
                #print("最近的距离：",smallest,smallest_index,"第二近的距离：",seclest,seclest_index)
                # 获取距离前一帧细胞距离+半径最接近的两个点及其index
                all_diff = sorted(all_diff.items(), key=lambda item: item[1])
                smallest = all_diff[0][1]
                smallest_index = all_diff[0][0]

                #print("最小值", smallest)
                if smallest <= biggest_diff:
                    # 找到了对应细胞
                    #在当前图像上画出两个细胞之间的连线
                    x=centers_radiu[smallest_index][0]
                    y=centers_radiu[smallest_index][1]
                    #保存每条连线所需要的点到list里，然后append进dict
                    tmp_list.append([(int(l_x),int(l_y)),(int(x),int(y))])
                    for key in cell_id_dict:
                        if cell_id_dict[key][-1]==[l_x,l_y]:
                            #这个细胞被注册过
                            #regist=True
                            cell_id_dict[key].append([x,y])
                            break

                else:
                    #没找到对应细胞
                    cell_id_dict[id] = [[x, y]]
                    id += 1

                # 获取距离前一帧细胞距离最近的两个点及其index
                diff_cen=sorted(diff_cen.items(), key=lambda item: item[1])
                max_dis = l_r  # 最大距离是原细胞的直径
                d_i=1
                flag=False
                while diff_cen[d_i][1]<=max_dis and flag==False:
                    frstlest = diff_cen[d_i-1][1]
                    frstlest_index = diff_cen[d_i-1][0]
                    s_i=1
                    while diff_cen[s_i][1] <= max_dis and flag==False:
                        seclest = diff_cen[s_i][1]
                        seclest_index = diff_cen[s_i][0]

                        ## 计算前一帧原始细胞的面积，和当前帧离这个原始细胞最近的两个细胞，如果面积和不大于原始细胞（因为腐蚀了），那这两个就是分裂的细胞
                        #print(k,last_img_center[k][3])
                        cnt0=forme_contours[last_img_center[k][3]]

                        cnt1=contours[centers_radiu[frstlest_index][3]]
                        cnt2=contours[centers_radiu[seclest_index][3]]
                        # 计算面积
                        cnt0_area=cv.contourArea(cnt0)
                        cnt1_area = cv.contourArea(cnt1)
                        cnt2_area = cv.contourArea(cnt2)
                        #half_blur_size=blur_size/2
                        # 原细胞面积-模糊值<两个细胞的面积和<原细胞面积+模糊值，并且距离不能大于原始细胞直径
                        if cnt1_area+cnt2_area<=cnt0_area+blur_size and cnt1_area+cnt2_area>=cnt0_area/2 \
                                and frstlest <= max_dis and seclest <= max_dis\
                                and cnt1_area <= (cnt0_area + blur_size) and cnt1_area >= (cnt0_area - blur_size)/6 \
                                and cnt2_area <= (cnt0_area + blur_size) and cnt2_area >= (cnt0_area - blur_size)/6 :
                            devid+=1
                            x, y, w, h = cv.boundingRect(cnt1)  # 绘制矩形外框
                            # 对normalize的图片标注
                            norimg = cv.rectangle(norimg, (x, y), (x + w, y + h), (0, 0, 255), 3)
                            x, y, w, h = cv.boundingRect(cnt2)  # 绘制矩形外框
                            # 对normalize的图片标注
                            norimg = cv.rectangle(norimg, (x, y), (x + w, y + h), (0, 0, 255), 3)
                            #画从这两个细胞到母细胞的线
                            cv.line(norimg, (last_img_center[k][0],last_img_center[k][1]),
                                     (centers_radiu[frstlest_index][0],centers_radiu[frstlest_index][1]), (0, 0, 255), 2)
                            cv.line(norimg, (last_img_center[k][0], last_img_center[k][1]),
                                     (centers_radiu[seclest_index][0], centers_radiu[seclest_index][1]),
                                     (0, 0, 255), 2)
                            tmp_list.append([(last_img_center[k][0],last_img_center[k][1]),
                                     (centers_radiu[frstlest_index][0],centers_radiu[frstlest_index][1])])
                            tmp_list.append([(last_img_center[k][0], last_img_center[k][1]),
                                     (centers_radiu[seclest_index][0], centers_radiu[seclest_index][1])])
                            flag=True
                            break
                        s_i+=1
                    d_i+=1
        else:
            #如果没有上一帧
            for cell in centers_radiu:
                x=cell[0]
                y=cell[1]
                cell_id_dict[id]=[[x,y]]
                id+=1

        if n>clear_time:
            n=1
        line_dict[n]=tmp_list
        for key in line_dict:
            if line_dict[key]!=[]:
                #print("line_dict[key]",line_dict[key])
                for line in line_dict[key]:
                    #print("line",line)
                    cv.line(norimg, line[0], line[1], (0, 255, 0), 1)
        cv.putText(norimg, f"The number of dividing cells is: {devid}", (10, 100), cv.FONT_HERSHEY_COMPLEX, 0.5,(100, 100, 200),1)


        if(track_open==True):
            # task3
            bbox = cv.selectROI('Tracker', norimg, False)
            print(bbox)
            if bbox != (0, 0, 0, 0):
                # 获取bbox的中点，寻找和他的中点距离最近的那个细胞
                b_x = bbox[0] + bbox[2] / 2
                b_y = bbox[1] + bbox[3] / 2
                b_tmp_list = {}
                for cell in centers_radiu:
                    c_x = cell[0]
                    c_y = cell[1]
                    c_id = cell[3]
                    b_tmp_list[(c_id,c_x,c_y)] = ed(np.array([c_x,c_y]),np.array([b_x,b_y]))
                b_tmp_list = sorted(b_tmp_list.items(), key=lambda item: item[1])
                sc_i = b_tmp_list[0][0][0]
                # 找到了最近距离的点的id，用contours画框，并传给下一个
                target_x = b_tmp_list[0][0][1]
                target_y = b_tmp_list[0][0][2]
                cnt_b = contours[centers_radiu[sc_i][3]]
                # print(b_tmp_list[0][1])
                x, y, w, h = cv.boundingRect(cnt_b)  # 绘制矩形外框
                # 对normalize的图片标注
                norimg = cv.rectangle(norimg, (x, y), (x + w, y + h), (255, 0, 0), 3)
                # 获取id_cell_dict中的值，计算路径
                speed = 0
                total_dis=0
                net_dis=0
                ratio=0
                for key in cell_id_dict:
                    if cell_id_dict[key][-1]==[target_x,target_y]:
                        # 计算task3
                        this_point=np.array(cell_id_dict[key][-1])
                        if len(cell_id_dict[key])>1:
                            last_point=np.array(cell_id_dict[key][-2])
                            speed = ed(this_point, last_point)
                        else:
                            speed=0
                        frst_point=np.array(cell_id_dict[key][0])
                        net_dis=ed(this_point,frst_point)
                        total_dis=0
                        for i in range(1,len(cell_id_dict[key])):
                            # 遍历这个细胞经过的每一个点
                            l_p=np.array(cell_id_dict[key][i-1])
                            t_p = np.array(cell_id_dict[key][i])
                            total_dis+=ed(l_p,t_p)
                        if net_dis == 0 or total_dis == 0:
                            ratio = 0
                        else:
                            ratio=net_dis/total_dis
                        break
                cv.putText(norimg, f"speed of the cell: {speed}", (10, 120), cv.FONT_HERSHEY_COMPLEX, 0.5,
                            (255, 255, 0), 1)
                cv.putText(norimg, f"total distance of the cell: {total_dis}", (10, 130), cv.FONT_HERSHEY_COMPLEX, 0.5,
                            (255, 255, 0), 1)
                cv.putText(norimg, f"net distance of the cell: {net_dis}", (10, 140), cv.FONT_HERSHEY_COMPLEX, 0.5,
                            (255, 255, 0), 1)
                cv.putText(norimg, f"ratio of the cell motion: {ratio}", (10, 150), cv.FONT_HERSHEY_COMPLEX, 0.5,
                            (255, 255, 0), 1)


        cv.imshow("final", norimg)
        cv.waitKey(0)
        cv.destroyWindow("Tracker")
        cv.destroyWindow("final")
        last_img_center=centers_radiu
        forme_contours=contours
        n+=1



def ed(m, n):
    return np.sqrt(np.sum((m - n) ** 2))




if __name__=='__main__':
    main()