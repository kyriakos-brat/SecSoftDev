using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace ConsoleApp1
{
    class Exercise2
    {
        public void Run()
        {
            FileInfo FI = new FileInfo("temp.txt");
            Console.WriteLine("\nFile. Enter any text:");
            CreateFile(FI);
            ReadFile(FI);

            Console.WriteLine("\nZIP");
            Exercise5 ex5 = new Exercise5();
            ex5.Run("temp.txt");

            FI.Delete();
        }
        public void CreateFile(FileInfo fileInfo)
        {
            using (FileStream FS = fileInfo.Create())
            {
                byte[] array = System.Text.Encoding.Default.GetBytes(Console.ReadLine());
                FS.Write(array, 0, array.Length);
            }
        }
        public void ReadFile(FileInfo fileInfo)
        {
            using (FileStream FS = fileInfo.OpenRead())
            {
                byte[] array = new byte[FS.Length];
                FS.Read(array, 0, array.Length);
                Console.WriteLine($"Text: {System.Text.Encoding.Default.GetString(array)}");
            }
        }
    }
}
