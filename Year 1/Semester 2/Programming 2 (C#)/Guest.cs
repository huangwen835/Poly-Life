using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace S10241971_PRG2Assignment
{
    class Guest
    {
        public string? Name { get; set; }
        public string? PassportNum { get; set; }
        public Stay? HotelStay { get; set; }
        public Membership? Member { get; set; }
        public bool IsCheckedin { get; set; }

        //Constructors
        public Guest() { }
        public Guest(string? name, string? passportNum, Stay? hotelStay, Membership? member)
        {
            Name = name;
            PassportNum = passportNum;
            HotelStay = hotelStay;
            Member = member;
        }
        //Methods
        public override string ToString()
        {
            return "Name: " + Name + "\tPassport Number: " + PassportNum + "\tMembership: " + Member + "\tChecked In: " + IsCheckedin
                + "\nStay: " + "\n" + HotelStay;
        }
    }
}
