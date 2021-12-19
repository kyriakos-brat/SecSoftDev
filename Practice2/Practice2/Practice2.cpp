// Practice2.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include <iomanip>
#include <sstream>
#include <vector>
#include <memory>
#include <thread>
#include <cmath>
#include <chrono>

#include "cryptlib.h"
#include "sha.h"
#include "filters.h"
#include "hex.h"
#include "files.h"
#include "misc.h"

#include <openssl/sha.h>

namespace bruteforce {
    constexpr static int BASE = 28;
    constexpr static int NUM_OF_SYMS = 5;
    constexpr static int ASCII_SHIFT = 'a';
    constexpr static int ASCII_BASE_SHIFT = 'A';
    static int NUM_OF_PERMUTATIONS = 0;
    std::map<std::string, std::string> hashesToFind{};
}

long ConvertTo10(const std::string& input, int base)
{
    if (base < 2 || base > 36)
        return 0;

    bool isNegative = (input[0] == '-');

    int startIndex = input.length() - 1;
    int endIndex = isNegative ? 1 : 0;

    long value = 0;
    int digitValue = 1;

    for (int i = startIndex; i >= endIndex; --i)
    {
        char c = input[i];

        // Uppercase it - NOTE: could be done with std::toupper
        if (c >= 'a' && c <= 'z')
            c -= ('a' - 'A');

        // Convert char to int value - NOTE: could be done with std::atoi
        // 0-9
        if (c >= '0' && c <= '9')
            c -= '0';
        // A-Z
        else
            c = c - 'A' + 10;

        if (c >= base)
            return 0;

        // Get the base 10 value of this digit    
        value += c * digitValue;

        // Each digit has value base^digit position - NOTE: this avoids pow
        digitValue *= base;
    }

    if (isNegative)
        value *= -1;

    return value;
}

std::string ConvertFrom10(long value, int base)
{
    if (base < 2 || base > 36)
        return "0";

    bool isNegative = (value < 0);
    if (isNegative)
        value *= -1;

    // NOTE: it's probably possible to reserve std::string based on value
    std::string output;

    do
    {
        char digit = value % base;

        // Convert to appropriate base character
        // 0-9
        if (digit < 10)
            digit += '0';
        // A-Z
        else
            digit = digit + 'A' - 10;

        // Append digit to std::string (in reverse order)
        output += digit;

        value /= base;

    } while (value > 0);

    if (isNegative)
        output += '-';

    // Reverse the std::string - NOTE: could be done with std::reverse
    int len = output.size() - 1;
    for (int i = 0; i < len; ++i)
    {
        // Swap characters - NOTE: Could be done with std::swap
        char temp = output[i];
        output[i] = output[len - i];
        output[len - i] = temp;
    }

    return output;
}

std::string sha256(const std::string str)
{
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, str.c_str(), str.size());
    SHA256_Final(hash, &sha256);
    std::stringstream ss;
    //for (int i = 0; i < SHA256_DIGEST_LENGTH; i++)
    //{
    //    ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    //}
    //return ss.str();
    static const char characters[] = "0123456789ABCDEF";
    std::string result(SHA256_DIGEST_LENGTH * 2, ' ');
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        result[2 * i] = characters[(unsigned int)hash[i] >> 4];
        result[2 * i + 1] = characters[(unsigned int)hash[i] & 0x0F];
    }
    return result;
}

int g_call_times = 0;

void bruteforceThread(unsigned long intervalStart, unsigned long invervalEnd)
{

    for (long i = intervalStart; i < invervalEnd; ++i) {
        g_call_times++;
        std::string baseStr = ConvertFrom10(i, bruteforce::BASE);
        std::string nonHashedStr{};

        for (int j = 0; j < baseStr.length(); ++j) {
            long baseStrSym = ConvertTo10(std::string(1, baseStr.at(j)), bruteforce::BASE);
            nonHashedStr.append(std::string(1, static_cast<char>(baseStrSym + bruteforce::ASCII_SHIFT)));
        }

        int padding = bruteforce::NUM_OF_SYMS - baseStr.length();
        if (padding) {
            for (int j = 0; j < padding; j++) {
                nonHashedStr.insert(0, "a");
            }
        }

        //CryptoPP::SHA256 hash;
        //std::string digest{};
        //hash.Update(reinterpret_cast<const CryptoPP::byte*>(nonHashedStr.data()), nonHashedStr.size());
        //digest.resize(hash.DigestSize());
        //hash.Final(reinterpret_cast<CryptoPP::byte*>(&digest[0]));
        ////
        //std::string strSink{};
        //CryptoPP::HexEncoder encoder(new CryptoPP::StringSink(strSink));
        //CryptoPP::StringSource(digest, true, new CryptoPP::Redirector(encoder));

        //std::string hashStr{ "hashPlease" };
        std::string strSink = sha256(nonHashedStr);

        auto findResult = bruteforce::hashesToFind.find(strSink);
        if (bruteforce::hashesToFind.end() != findResult) {
            //WARNING!! Here should be mutex cause many threads can attempt to modify container
            findResult->second = nonHashedStr;
            std::cout << "For hash " << findResult->first << " password is " << findResult->second << std::endl;
        }
    }
}

int main()
{
    bruteforce::NUM_OF_PERMUTATIONS = std::pow(bruteforce::BASE, bruteforce::NUM_OF_SYMS);

    bruteforce::hashesToFind.insert({ "1115DD800FEAACEFDF481F1F9070374A2A81E27880F187396DB67958B207CBAD", "" });
    bruteforce::hashesToFind.insert({ "3A7BD3E2360A3D29EEA436FCFB7E44C735D117C42D1C1835420B6B9942DD4F1B", "" });
    bruteforce::hashesToFind.insert({ "74E1BB62F8DABB8125A58852B63BDF6EAEF667CB56AC7F7CDBA6D7305C50A22F", "" });

    //bruteforce::hashesToFind.insert({ "ED968E840D10D2D313A870BC131A4E2C311D7AD09BDF32B3418147221F51A6E2", ""});
    //bruteforce::hashesToFind.insert({ "38790A1FF4CE8539D251D5C1F7C3F2D68E5C9BE12DCAD38AE64854C439732615", ""});
    //bruteforce::hashesToFind.insert({ "8A4598AA5D2C0C3512BF4354921E146768717C1844FE3A6445C44AD1183AD495", ""});

    std::cout << "Enter number of threads\n";
    int numOfThreads{ 0 };
    std::cin >> numOfThreads;
    if (numOfThreads < 0) {
        std::cout << "Incorrect number of threads!" << std::endl;
    }

    auto start = std::chrono::high_resolution_clock::now();
    //bruteforceThread(0, 100000);
    //int rrr = 0;

    std::vector<std::thread> threads;

    long intervalGap = bruteforce::NUM_OF_PERMUTATIONS / numOfThreads;
    long currentGap{ 0 };

    for (int i = 0; i < numOfThreads; ++i) {
        long nextGap = currentGap + intervalGap;
        threads.push_back(std::thread(bruteforceThread, currentGap, nextGap));
        currentGap = nextGap;
    }

    for (std::thread& thread : threads) {
        thread.join();
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "Duration is " << duration.count() << "ms" << std::endl;
    //std::cout << "Call count is " << g_call_times << std::endl;
}
