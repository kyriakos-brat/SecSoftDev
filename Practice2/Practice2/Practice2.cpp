// Practice2.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include <vector>
#include <memory>
#include <thread>

#include "cryptlib.h"
#include "sha.h"
#include "filters.h"
#include "hex.h"
#include "files.h"

int main()
{
    std::cout << "Enter number of threads\n";
    int numOfThreads{ 0 };
    std::cin >> numOfThreads;

    std::string testStr{ "HEre is my test string" };
    std::string digest{};

    CryptoPP::SHA256 hash;
    hash.Update(reinterpret_cast<const CryptoPP::byte*>(testStr.data()), testStr.size());
    digest.resize(hash.DigestSize());
    hash.Final(reinterpret_cast<CryptoPP::byte*>(&digest[0]));

    CryptoPP::HexEncoder encoder(new CryptoPP::FileSink(std::cout));
    std::cout << "Message: " << testStr << std::endl;

    std::cout << "Digest: ";
    CryptoPP::StringSource(digest, true, new CryptoPP::Redirector(encoder));
    std::cout << std::endl;

    //std::vector<std::thread> threads;
    //for (int i = 0; i < numOfThreads; ++numOfThreads) {
    //    threads.push_back(std::thread());
    //}

    //for (std::thread& thread : threads) {
    //    thread.join();
    //}
}

// Запуск программы: CTRL+F5 или меню "Отладка" > "Запуск без отладки"
// Отладка программы: F5 или меню "Отладка" > "Запустить отладку"

// Советы по началу работы 
//   1. В окне обозревателя решений можно добавлять файлы и управлять ими.
//   2. В окне Team Explorer можно подключиться к системе управления версиями.
//   3. В окне "Выходные данные" можно просматривать выходные данные сборки и другие сообщения.
//   4. В окне "Список ошибок" можно просматривать ошибки.
//   5. Последовательно выберите пункты меню "Проект" > "Добавить новый элемент", чтобы создать файлы кода, или "Проект" > "Добавить существующий элемент", чтобы добавить в проект существующие файлы кода.
//   6. Чтобы снова открыть этот проект позже, выберите пункты меню "Файл" > "Открыть" > "Проект" и выберите SLN-файл.
