using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    class Exercise5
    {
        public void Run(string path)
        {
            string sourceFile = path;
            string compressedFile = "temp.gz";
            string targetFile = "temp_new.txt";

            Compress(sourceFile, compressedFile);
            Decompress(compressedFile, targetFile);

            Console.WriteLine("Unzipped file text:");
            Exercise2 fileWorker = new Exercise2();
            FileInfo fileInfo = new FileInfo(targetFile);
            fileWorker.ReadFile(fileInfo);
            fileInfo.Delete();

            FileInfo compressed = new FileInfo(compressedFile);
            compressed.Delete();
        }
        public static void Compress(string sourceFile, string compressedFile)
        {
            using (FileStream sourceStream = new FileStream(sourceFile, FileMode.OpenOrCreate))
            {
                using (FileStream targetStream = File.Create(compressedFile))
                {
                    using (GZipStream compressionStream = new GZipStream(targetStream, CompressionMode.Compress))
                    {
                        sourceStream.CopyTo(compressionStream);
                        Console.WriteLine("Zipped {0} successfully. Source size: {1}  zipped size: {2}.",
                            sourceFile, sourceStream.Length.ToString(), targetStream.Length.ToString());
                    }
                }
            }
        }

        public static void Decompress(string compressedFile, string targetFile)
        {
            using (FileStream sourceStream = new FileStream(compressedFile, FileMode.OpenOrCreate))
            {
                using (FileStream targetStream = File.Create(targetFile))
                {
                    using (GZipStream decompressionStream = new GZipStream(sourceStream, CompressionMode.Decompress))
                    {
                        decompressionStream.CopyTo(targetStream);
                        Console.WriteLine("Unzipped text: {0}", targetFile);
                    }
                }
            }
        }
    }
}
