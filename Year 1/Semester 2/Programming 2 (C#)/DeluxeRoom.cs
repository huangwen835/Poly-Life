using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace S10241971_PRG2Assignment
{
    class DeluxeRoom : Room
    {
        public bool AdditionalBed { get; set; }

        public DeluxeRoom() { }

        public DeluxeRoom(int rn, string? bc, double rd, bool ia) : base(rn, bc, rd, ia) { }

        public override double CalculateCharges()
        {
            if (AdditionalBed)
            {
                return DailyRate + 25;
            }
            return DailyRate;
        }

        public override string ToString()
        {
            return base.ToString() +
                "\tAdditional Bed: " + AdditionalBed;
        }
    }
}
