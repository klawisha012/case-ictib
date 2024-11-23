#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

int main(int argc, char* argv[]) {
    // Проверяем, что переданы два аргумента
    if (argc != 3) {
        std::cerr << "Usage: app.exe <input_file> <output_file>" << std::endl;
        return 1; // Ошибка: неправильное количество аргументов
    }

    std::string inputFilePath = argv[1];
    std::string outputFilePath = argv[2];

    // Проверяем, существует ли входной файл
    if (!std::filesystem::exists(inputFilePath)) {
        std::cerr << "Error: Input file does not exist: " << inputFilePath << std::endl;
        return 2; // Ошибка: входной файл не найден
    }

    try {
        // Открываем входной и выходной файлы
        std::ifstream inputFile(inputFilePath, std::ios::binary);
        std::ofstream outputFile(outputFilePath, std::ios::binary);

        // Проверяем, удалось ли открыть файлы
        if (!inputFile.is_open()) {
            std::cerr << "Error: Cannot open input file: " << inputFilePath << std::endl;
            return 3; // Ошибка: входной файл недоступен
        }
        if (!outputFile.is_open()) {
            std::cerr << "Error: Cannot create output file: " << outputFilePath << std::endl;
            return 4; // Ошибка: выходной файл недоступен
        }

        // Копируем содержимое
        outputFile << inputFile.rdbuf();

        // Успешная обработка
        std::cout << "Processing complete. File saved to: " << outputFilePath << std::endl;
        return 0; // Успех
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 5; // Ошибка: исключение
    }
}
