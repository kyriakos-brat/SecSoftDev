using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    class User
    {
        public string Name { get; set; }
        public int Age { get; set; }
        public string Course { get; set; }
    }
    class Exercise4
    {
        public void Run()
        {
            Console.WriteLine("\nJSON. Enter name:");
            string name = Console.ReadLine();
            Console.WriteLine("Enter age:");
            int age = int.Parse(Console.ReadLine());
            Console.WriteLine("Enter course:");
            SerialazeJSON(name, age, Console.ReadLine());
            DeserialazeJSON();
        }

        public static void SerialazeJSON(string name, int age, string course)
        {
            using (StreamWriter file = File.CreateText("temp.json"))
            {
                User us = new User() { Name = name, Age = age, Course = course };
                JsonSerializer serializer = new JsonSerializer();
                serializer.Serialize(file, us);
                Console.WriteLine("Saved.");
            }
        }
        public static void DeserialazeJSON()
        {
            using (StreamReader file = File.OpenText("temp.json"))
            {
                JsonSerializer serializer = new JsonSerializer();
                User user1 = (User)serializer.Deserialize(file, typeof(User));
                Console.WriteLine($"Name: {user1.Name}  Age: {user1.Age} Course: {user1.Course}");
            }
        }
    }
}
