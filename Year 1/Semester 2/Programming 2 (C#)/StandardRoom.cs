using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace S10241971_PRG2Assignment
{
    class StandardRoom : Room
    {
        public bool RequireWifi { get; set; }

        public bool RequireBreakfast { get; set; }

        public StandardRoom() { }

        public StandardRoom(int rn, string? bc, double dr, bool ia) : base(rn, bc, dr, ia) { }

        public override double CalculateCharges()
        {
            if (RequireWifi == true && RequireBreakfast == true)
            {
                return DailyRate + 10 + 20;
            }
            else if (RequireWifi)
            {
                return DailyRate + 10;
            }
            else if (RequireBreakfast)
            {
                return DailyRate + 20;
            }
            return DailyRate;
        }

        public override string ToString()
        {
            return base.ToString() +
                "\tRequire Wifi: " + RequireWifi +
                "\tRequire Breakfast: " + RequireBreakfast;
        }
    }
}
