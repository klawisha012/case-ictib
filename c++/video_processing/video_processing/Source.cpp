// #include <opencv2/core.hpp>
// #include <opencv2/highgui.hpp>
// #include <opencv2/imgproc.hpp>
// #include <string>

// using namespace cv;
// using namespace std;

// int main()
// {
//     // �������� ����������� �������� 500x400
//     Mat img(400, 500, CV_8UC3);

//     // ����� ��� �����������
//     string text = "Hello World!";

//     // ������������� ������
//     Point textOrg(100, img.rows / 2);

//     // ��������� ������
//     int fontFace = FONT_HERSHEY_SCRIPT_SIMPLEX;
//     double fontScale = 2;
//     Scalar color(200, 100, 50); // ���� ������

//     // ��������� ������ �� �����������
//     putText(img, text, textOrg, fontFace, fontScale, color);

//     // ����������� �����������
//     imshow("My World", img);
//     waitKey(0);

//     return 0;
// }
