import numpy as np
import cv2


MIN_MATCH_COUNT = 7
# 추적 대상 이미지
img1 = cv2.imread('testcard.jpg')
img1 = cv2.resize(img1,(514,811), interpolation=cv2.INTER_AREA)

# SIFT 객체 생성
sift = cv2.SIFT_create(nfeatures=5000)
kp1, des1 = sift.detectAndCompute(img1, None)

# 비디오 
vdo = cv2.VideoCapture('testcard.mp4')

# FPS 계산
fps = vdo.get(cv2.CAP_PROP_FPS)
delay_ms = int(1000/fps) if fps > 0 else 1

# 매칭
bf = cv2.BFMatcher(cv2.NORM_L2)

while(True):
    ret, frame = vdo.read()
    if not ret:
        break
    
    # 영상 크기 조절
    frame = cv2.resize(frame, (720,720), interpolation=cv2.INTER_AREA)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # SIFT 특징점 검출
    kp2, des2 = sift.detectAndCompute(gray_frame, None)
    
    # 좋은 매칭점 필터링
    
    if des2 is not None and len(des2) > 0:
        matches = bf.knnMatch(des1, des2, k=2)
        
        good_matches = []
        if matches:
            for m, n in matches:
                # 1 순위 매칭이 2 순위 매칭보다 훨씬 가까울 때만 채택
                if m.distance < 0.85 * n.distance:
                    good_matches.append(m)
        
        # 좋은 매칭점들을 거리가 가까운 순으로 정렬
        good_matches = sorted(good_matches, key=lambda x: x.distance)
        # 테두리 그리기
        # 좋은 매칭점이 10개 이상일 때문 추적 수행
        if len(good_matches) > 10:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)

            # Homography 행렬 계산
            
            M, mask = cv2.findHomography(src_pts,dst_pts, cv2.RANSAC, 10.0)
            
            if M is not None:
                #기준 이미지의 모서리 좌표를 영상 속 위치로 변환
                h, w , _ = img1.shape
                pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts, M)
                
                # 객체 주위에 초록색 테두리 그리기
                frame = cv2.polylines(frame, [np.int32(dst)], True, (0,255,0),3,cv2.LINE_AA)
        
        # 매칭 결과를 초록색 단색 선으로 연결
        output_frame = cv2.drawMatches(
                img1, kp1, frame, kp2, good_matches[:10], 
                None, matchColor=(0, 255, 0), singlePointColor=(0, 255, 0), flags=2
            )
        cv2.imshow('SIFT Tracking Result', output_frame)
    else:
        # 특징점 검출 실패 했을 때 원본 표시
        cv2.imshow('SIFT Tracking Result',frame)
        
    # FPS 대기 설정
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원해제
vdo.release()
cv2.destroyAllWindows()
    
    