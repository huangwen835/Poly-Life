using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace S10241971_PRG2Assignment
{
    class Stay
    {
        public DateTime CheckInDate { get; set; }

        public DateTime CheckOutDate { get; set; }

        public List<Room> RoomList { get; set; } = new List<Room>();

        public Stay() { }

        public Stay(DateTime cid, DateTime cod)
        {
            CheckInDate = cid;
            CheckOutDate = cod;
            RoomList = new List<Room>();    
        }

        public void AddRoom(Room r)
        {
            bool found = false;
            foreach (Room room in RoomList)
            {
                if(room == r)
                {
                    found = true;
                    Console.WriteLine("Room alr added.");
                    break;
                }
            }    
            if (!found)
            {
                RoomList.Add(r);
            }
        }

        public double CalculateTotal()
        {
            double total = 0;
            int datediff = Convert.ToInt32((CheckOutDate - CheckInDate).TotalDays);
            foreach (Room r in RoomList)
            {
                total += r.CalculateCharges() * datediff;
            }
            return total;
        }

        public override string ToString()
        {
            string rdetail = "";
            foreach (Room r in RoomList)
            {
                rdetail += r.ToString() + "\n";
            }
            return "Check in Date: " +
                CheckInDate + "\tCheck Out Date: " +
                CheckOutDate + "\nRoom List: \n" + rdetail;
        }
    }
}

