using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace S10241971_PRG2Assignment
{
    class Membership
    {
        public string? Status { get; set; }

        public int Points { get; set; }

        public Membership() { }

        public Membership(string? s, int p)
        {
            Status = s;
            Points = p;
        }

        public void EarnPoints(double amt)
        {
            Points += (int)(amt / 10);
            if (Points >= 100 && Status == "Ordinary" && Points < 200)
            {
                Status = "Silver";
                Console.WriteLine("Points reach " + Points + ", " +
                    "membership status upgrade to Silver.");
            }
            else if (Points >= 200 && (Status == "Sliver" || Status =="Ordinary"))
            {
                Status = "Gold";
                Console.WriteLine("Points reach " + Points + ", " +
                    "membership status upgrade to Gold.");
            }
        }

        public bool RedeemPoints(int p)
        {
            if (Points < p)
            {
                Console.WriteLine("Not enough points!");
                return false;
            }
            Points -= p;
            Console.WriteLine("Points successfully deducted!");
            return true;
        }

        public override string ToString()
        {
            return "Status: " + Status +
                "\tPoints: " + Points;
        }
    }
}
