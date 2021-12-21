using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace ConsoleApp1
{
    class Exercise1
    {
        public void Run()
        {
            DriveInfo[] allDrives = DriveInfo.GetDrives();

            foreach (DriveInfo d in allDrives)
            {
                Console.WriteLine("Drive {0}", d.Name);
                Console.WriteLine("  Type: {0}", d.DriveType);
                if (d.IsReady == true)
                {
                    Console.WriteLine("  Mark: {0}", d.VolumeLabel);
                    Console.WriteLine("  File system: {0}", d.DriveFormat);
                    Console.WriteLine(
                        "  Disk size:            {0, 15} bytes ",
                        d.TotalSize);
                }
            }
        }
    }
}
