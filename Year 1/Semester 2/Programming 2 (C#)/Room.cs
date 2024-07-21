using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace S10241971_PRG2Assignment
{
    abstract class Room
    {
        public int RoomNumber { get; set; }

        public string? BedConfiguration { get; set; }

        public double DailyRate { get; set; }

        public bool IsAvail { get; set; }

        public Room() { }

        public Room(int rn, string? bc, double dr, bool ia) { RoomNumber = rn; BedConfiguration = bc; DailyRate = dr; IsAvail = ia; }

        public abstract double CalculateCharges();

        public override string ToString()
        {
            return "Room Number: " + RoomNumber + "\tBed Configuration: "
                + BedConfiguration + "\tDaily Rate: "
                + DailyRate + "\tIs Available: " + IsAvail;
        }

    }
}
