def get_iou(box1,box2):
    xa = max(box1[0],box2[0])
    ya = max(box1[1],box2[1])
    xb = min(box1[2],box2[2])
    yb = min(box1[3],box2[3])

    inter = max(0,xb - xa + 1) * max(0,yb - ya + 1)
    area1 = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    area2 = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)
    iou = inter / (area2 + area1 - inter)

    return iou
