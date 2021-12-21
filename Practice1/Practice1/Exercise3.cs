using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Serialization;

namespace ConsoleApp1
{
    [Serializable]
    public class Person
    {
        public string Name { get; set; }
        public int Age { get; set; }
        public string Course { get; set; }

        public Person()
        { }

        public Person(string name, int age, string course)
        {
            Name = name;
            Age = age;
            Course = course;
        }
    }
    class Exercise3
    {
        public void Run()
        {
            Console.WriteLine("\nXML. Enter name:");
            string name = Console.ReadLine();
            Console.WriteLine("Enter age:");
            int age = int.Parse(Console.ReadLine());
            Console.WriteLine("Enter course:");
            SerealizeXML(name,age,Console.ReadLine());
            Console.WriteLine("XML-file created. \nXML-file content:");
            DeserealizeXML();
            FileInfo FD = new FileInfo("temp.xml");
            FD.Delete();
        }
        public static void SerealizeXML(string name, int age, string company)
        {
            Person person = new Person(name, age, company);
            Person[] people = new Person[] { person };

            XmlSerializer formatter = new XmlSerializer(typeof(Person[]));

            using (FileStream fs = new FileStream("temp.xml", FileMode.OpenOrCreate))
            {
                formatter.Serialize(fs, people);
            }
        }
        public static void DeserealizeXML()
        {
            //первый способ десериализации
            XmlSerializer formatter = new XmlSerializer(typeof(Person[]));
            using (FileStream fs = new FileStream("temp.xml", FileMode.OpenOrCreate))
            {
                Person[] newpeople = (Person[])formatter.Deserialize(fs);

                foreach (Person p in newpeople)
                {
                    Console.WriteLine($"Name: {p.Name} --- Age: {p.Age} --- Course: {p.Course}");
                }
            }
        }
    }
}
