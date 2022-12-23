# Escape-problem

![image](https://user-images.githubusercontent.com/58596222/209365696-9857a64a-aa16-48e8-9ff8-d7e6465492e0.png)

- n * n 그리드 형태의 무방향 그래프가 존재한다. 행렬을 (i, j)로 표현했을 때, 그리드의 i =1, i = n, j =1, or j = n(테두리에 위치한 정점들)을 제외한 모든 정점들은 정확히 4개의 이웃을 갖는다.

- 시작점은 검은색, 다른 정점들은 흰색이다. (a) 그래프의 탈출 경로는 그림자로 표현된 경로이며, (b) 그래프는 탈출 불가능하다.

- 탈출 문제는 그리드에서 시작점 (x1, y1), (x2, y2), …, (xm, ym)이 주어졌을 때 각 시작점에서 경계로 가는 m개의 경로가 존재하는지 여부를 결정한다.

## 동작 순서

|      | 동작                                                         | 시각화                                                       |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1    | • 모든 간선에 1의 가중치를 부여한다                          | ![image](https://user-images.githubusercontent.com/58596222/209365734-70475dc7-3e5c-4aa5-9d35-58bd1ee15263.png)
| 2    | • 정점 s를 만든다.  • 모든 시작점에 방향 연결한다.  • 새로 만든 간선에 1의 가중치를 부여한다. | ![image](https://user-images.githubusercontent.com/58596222/209365750-149cfd3f-7835-449c-9ca1-e5309f8bc6a6.png)
| 3    | • 정점 t를 만든다.  • 그리드의 경계에 있는  정점들을 t에 방향 연결한다.  • 간선에 1의 가중치를 부여한다. | ![image](https://user-images.githubusercontent.com/58596222/209365759-008f15d0-db12-4760-8795-4327a6bae558.png)
| 4    | • 정점에는 Cost가 없기 때문에 정점을 통한 경로가 중복되는  경우가 발생할 수 있는데, 그리드를 2중으로 만들어 Vin과 Vout을 만든 후, 간선의  가중치를 1로 부여해 해결한다. | ![image](https://user-images.githubusercontent.com/58596222/209365778-8e23f993-b7b2-4496-88ed-48c2b93dc288.png)
| 5    | • Network Flow의 입력 인스턴스로 변형하였으므로 Edmonds-Karp  알고리즘으로 이를 풀 수 있다.  • Network Flow 문제를 알려진 방법대로 푼다.  • 결과로 나온 max flow는  robbers의 수와 동일하다.  • flow들의 0또는 1의  값은 모든 정점들에 대한 탈출 경로를 나타낸다. | -                                                            |

## 출력 예

| 입력 데이터                                                  | 콘솔 결과                                                    |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![image](https://user-images.githubusercontent.com/58596222/209365817-f7a8d0d4-3d8e-408c-b31e-bb987ac123e6.png)![image](https://user-images.githubusercontent.com/58596222/209366260-c15ff46b-6f1c-40f2-8bdc-bbdebb724a78.png) | ![image](https://user-images.githubusercontent.com/58596222/209366314-8119fa6b-03b6-410b-ae7d-72485b49d56d.png) |
