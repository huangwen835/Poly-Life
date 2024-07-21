// See https://aka.ms/new-console-template for more information

using S10241971_PRG2Assignment;
using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Diagnostics;
using System.Linq.Expressions;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Xml.Serialization;

List<Guest> guestList = new List<Guest>();
List<Room> roomList = new List<Room>();
ReadRoom(roomList);
ReadGuest(guestList, roomList);


while (true)
{
    DisplayMenu();
    string? choice = Console.ReadLine();
    if (choice == "1")
    {
        DisplayGuestAllInfo(guestList);
    }
    else if (choice == "2")
    {
        DisplayAvailRoom(roomList); //Supposed to display available rooms

    }
    else if (choice == "3")
    {
        RegisterGuest(guestList);
    }
    else if (choice == "4")
    {
        int num = DisplayGuest(guestList);
        CheckIn(guestList, roomList, num);
    }
    else if (choice == "5")
    {
        int num = DisplayGuest(guestList);
        GuestStaydetails(guestList, num);
    }
    else if (choice == "6")
    {
        int num = DisplayGuest(guestList);
        ExtendStay(guestList, num);
    }
    else if (choice == "7")
    {
        List<string> monthList = InitmList();
        List<double> monthamtList = InitmaList();
        Calyear(guestList, monthList, monthamtList);
    }
    else if (choice == "8")
    {
        int num = DisplayGuest(guestList);
        CheckOut(guestList, roomList, num);
    }
    else if (choice == "0")
    {
        break;
    }
    else
    {
        Console.WriteLine("Incorrect input");
    }
}

void DisplayMenu()
{
    Console.WriteLine();
    Console.WriteLine("---------------- M E N U -----------------");
    Console.WriteLine("[1] List all guest");
    Console.WriteLine("[2] List all available rooms");
    Console.WriteLine("[3] Register guest");
    Console.WriteLine("[4] Check-in guest");
    Console.WriteLine("[5] Display stay details of a guest");
    Console.WriteLine("[6] Extends stay");
    Console.WriteLine("[7] Display monthly charged amounts " +
        "breakdown & total charged amounts for the year");
    Console.WriteLine("[8] Check out guest");
    Console.WriteLine("------------------------------------------");
    Console.Write("Enter your option: ");
}

// Methods

void ReadRoom(List<Room> rList)
{
    string[] csvLines = File.ReadAllLines("Rooms.csv");
    for (int i = 1; i < csvLines.Length; i++)
    {
        string[] all = csvLines[i].Split(',');
        string roomtype = all[0];
        int Roomnum = Convert.ToInt32(all[1]);
        string BedConfig = all[2];
        double Rate = Convert.ToDouble(all[3]);
        
        if (roomtype == "Standard")
        {
            rList.Add(new StandardRoom(Roomnum, BedConfig, Rate, true));
        }
        else
        {
            rList.Add(new DeluxeRoom(Roomnum, BedConfig, Rate, true));
        }
    }
}

void ReadGuest(List<Guest> gList, List<Room> rList)
{
    string[] csvLines1 = File.ReadAllLines("Guests.csv");
    for (int i = 1; i < csvLines1.Length; i++)
    {
        string[] all1 = csvLines1[i].Split(',');
        string name = all1[0];
        string passport = all1[1];
        Membership m = new Membership(all1[2], Convert.ToInt32(all1[3]));

        Guest g = new Guest(name, passport, null, m);
        string[] csvLines2 = File.ReadAllLines("Stays.csv");
        for (int j = 0; j < csvLines2.Length; j++)
        {
            string[] all2 = csvLines2[j].Split(',');
            if (all2[1] == passport)
            {
                Stay s = new Stay(Convert.ToDateTime(all2[3]), Convert.ToDateTime(all2[4]));
                int column = 5;
                while (column <= 9)
                {
                    if (all2[column] == "")
                    {
                        break;
                    }
                    else
                    {
                        foreach (Room r in rList)
                        {
                            if (r.RoomNumber == Convert.ToInt32(all2[column]))
                            {
                                if (all2[2] == "TRUE")
                                {
                                    r.IsAvail = false;
                                    g.IsCheckedin = true;
                                }
                                if (r is StandardRoom)
                                {
                                    StandardRoom sr = new StandardRoom(r.RoomNumber, r.BedConfiguration, r.DailyRate, r.IsAvail);
                                    sr.RequireWifi = Convert.ToBoolean(all2[column + 1]);
                                    sr.RequireBreakfast = Convert.ToBoolean(all2[column + 2]);
                                    s.AddRoom(sr);
                                }
                                else
                                {
                                    DeluxeRoom dr = new DeluxeRoom(r.RoomNumber, r.BedConfiguration, r.DailyRate, r.IsAvail);
                                    dr.AdditionalBed = Convert.ToBoolean(all2[column + 3]);
                                    s.AddRoom(dr);
                                }
                                break;
                            }
                        }
                    }
                    column += 4;

                }
                g.HotelStay = s;
                break;
            }
        }
        gList.Add(g);
    }
}

//Display Lists
int DisplayGuest(List<Guest> gList)
{
    int num = 1;
    foreach (Guest g in gList)
    {
        Console.WriteLine("[{0,0}] {1,-10}", num, g.Name);
        num++;
    }
    return num;
} 

void DisplayGuestAllInfo(List<Guest> gList)
{
    Console.WriteLine("{0,-10} {1,-12} {2,-10} {3,-15} {4,-10}", "Name", "PassportNum", "Status", "Member Points", "Checked In");
    foreach (Guest g in gList)
    {
        Console.WriteLine("{0,-10} {1,-12} {2,-10} {3,-15} {4,-10}", g.Name, g.PassportNum, g.Member.Status, g.Member.Points, g.IsCheckedin);
    }
}

void DisplayAvailRoom(List<Room> rList)
{
    int num = 1;
    Console.WriteLine("{0,-3} {1,-15} {2,-15} {3,-20} {4,-10}",
                    "", "Room type", "Room Number", "Bed Configuration", "Daily Rate");
    foreach (Room r in rList)
    {
        if (r.IsAvail == true)
        {
            if (r is StandardRoom)
            {
                Console.WriteLine("[{0,0}] {1,-15} {2,-15} {3,-20} {4,-10}",
                    num, "Standard Room", r.RoomNumber, r.BedConfiguration, r.DailyRate);
            }
            else
            {
                Console.WriteLine("[{0,0}] {1,-15} {2,-15} {3,-20} {4,-10}",
                    num, "Deluxe Room", r.RoomNumber, r.BedConfiguration, r.DailyRate);
            }
            num++;
        }
    }
}

int DisplayAvailRoom2(List<Room> rList)
{
    List<Room> roomList = new List<Room>();
    int num = 1;
    foreach (Room r in rList)
    {
        if (r.IsAvail == true)
        {
            if (r is StandardRoom)
            {
                Console.WriteLine("[{0,0}] {1,-15} {2,-7} {3,-7} {4,-10}",
                    num, "Standard Room", r.RoomNumber, r.BedConfiguration, r.DailyRate);
                roomList.Add(new StandardRoom(r.RoomNumber, r.BedConfiguration, r.DailyRate, true));
            }
            else
            {
                Console.WriteLine("[{0,0}] {1,-15} {2,-7} {3,-7} {4,-10}",
                    num, "Deluxe Room", r.RoomNumber, r.BedConfiguration, r.DailyRate);
                roomList.Add(new DeluxeRoom(r.RoomNumber, r.BedConfiguration, r.DailyRate, true));
            }
            num++;
        }
    }
    return num;
}


//Other Method
void RegisterGuest(List<Guest> guestList)
{
    Guest g = new Guest();
    while (true)
    {
        Console.Write("Enter guest name: ");
        string name = Console.ReadLine();
        g.Name = name;
        if (name.All(Char.IsLetter) == false || name == "")
        {
            Console.WriteLine("Invalid name!");
        }
        else 
        {
            g.Name = name;
            break; }
    }

    bool allpass = true;
    

    //While loop to propmt user infinetly if he input passport num wrgly
    while (allpass)
    {
        //all pass is to validate evry parts of passportnum
        allpass = false;
        Console.Write("Enter passport number: ");
        string passportNum = Console.ReadLine();
        int len = passportNum.Count();
        if (len != 9)
        {
            Console.WriteLine("Passport number length must be 9 characters long!");
            allpass = true;
        }
        else if (!(Char.IsLetter(passportNum[0]) == true && Char.IsLetter(passportNum[8]) == true))
        {
            Console.WriteLine("Invalid format!");
            allpass = true;
        }
        else
        {
            //Validate if the inbetween is all numeric num
            bool pass = true;
            for (int i = 1; i < (len - 2); i++)
            {
                if (Char.IsNumber(passportNum[i]) == false)
                {
                    pass = false;
                    break;
                }
            }
            if (pass == false)
            {
                Console.WriteLine("Invalid format!");
                allpass = true;

            }
        } 
        if (allpass == false)
        {
            passportNum = passportNum.ToUpper();
            g.PassportNum = passportNum;
            break;
        }
    }



    //forloop guests to see if passport num inside list
    bool found = false;
    foreach (Guest guest in guestList)
    {
        if (guest.PassportNum == g.PassportNum)
        {
            Console.WriteLine("Guest already registered");
            found = true;
            break;
        }
    }
    if (found == false)
    {
        Membership m = new Membership("Ordinary", 0);
        g.Member = m;
        guestList.Add(g);
        g.IsCheckedin = false;
        string data = g.Name + "," + g.PassportNum + "," + "Ordinary" + "," + "0";
        using (StreamWriter sw = new StreamWriter("Guests.csv", true))
        {
            sw.WriteLine(data);
        }
        Console.WriteLine("Registeration is successful!");
    }

}

void CheckIn(List<Guest> gList, List<Room> rList, int num)
{
    int choice = 0;
    while (true)
    {
        Console.Write("Enter your option: ");
        try
        {
            choice = Convert.ToInt32(Console.ReadLine());
            if (choice >= 1 && choice <= (num - 1))
            {
                break;
            }
            else
            {
                Console.WriteLine("Invalid option");
            }
        }
        catch (System.FormatException)
        {
            Console.WriteLine("Invalid option");
        } 
    }
    Stay s = new Stay();
    while (true)
    {
        try
        {
            Console.Write("Enter check in date: ");
            DateTime cid = Convert.ToDateTime(Console.ReadLine());
            s.CheckInDate = cid;
            break;
        }
        catch (System.FormatException)
        {
            Console.WriteLine("Invalid input");
        }
        
    }
    while (true)
    {
        try
        {
            Console.Write("Enter check out date: ");
            DateTime cod = Convert.ToDateTime(Console.ReadLine());
            if (s.CheckInDate >= cod)
            {
                Console.WriteLine("Check" +
                    " out date must be later then check in date!");
            }
            else
            {
                s.CheckOutDate = cod;
                break;
            }
        }
        catch (System.FormatException)
        {
            Console.WriteLine("Invalid input");
        }

    }

    bool anotherroom = true;
    while (true)
    {
        int arnum = DisplayAvailRoom2(roomList);
        int rchoice = 0;
        while (true)
        {
            Console.Write("Enter your room option: ");
            try
            {
                rchoice = Convert.ToInt32(Console.ReadLine());
                if (rchoice >= 1 && rchoice <= (arnum - 1))
                {
                    break;
                }
                else
                {
                    Console.WriteLine("Invalid option");
                }
            }
            catch (System.FormatException)
            {
                Console.WriteLine("Invalid option");
            }

        }
        rchoice -= 1;
        int ri = 0;
        foreach (Room r in rList)
        {
            if (r.IsAvail == true)
            {
                if (ri == rchoice)
                {
                    r.IsAvail = false;
                    if (r is StandardRoom)
                    {
                        StandardRoom sr = new StandardRoom(r.RoomNumber,
                            r.BedConfiguration, r.DailyRate, r.IsAvail);
                        while (true)
                        {
                            Console.Write("Require Wifi[Y/N]: ");
                            string? wifi = Console.ReadLine();
                            if (wifi == "Y" || wifi == "N")
                            {
                                if (wifi == "Y")
                                {
                                    sr.RequireWifi = true;
                                }
                                else
                                {
                                    sr.RequireWifi = false;
                                }
                                break;
                            }
                            else
                            {
                                Console.WriteLine("Invalid input.");
                            }
                        }
                        while (true)
                        {
                            Console.Write("Require Breakfast[Y/N]: ");
                            string? bf = Console.ReadLine();
                            if (bf == "Y" || bf == "N")
                            {
                                if (bf == "Y")
                                {
                                    sr.RequireBreakfast = true;
                                }
                                else
                                {
                                    sr.RequireBreakfast = false;
                                }
                                break;
                            }
                            else
                            {
                                Console.WriteLine("Invalid input.");
                            }
                        }
                        s.AddRoom(sr);
                    }
                    else
                    {
                        DeluxeRoom dr = new DeluxeRoom(r.RoomNumber,
                            r.BedConfiguration, r.DailyRate, r.IsAvail);
                        while (true)
                        {
                            Console.Write("Require Additional Bed[Y/N]: ");
                            string? ab = Console.ReadLine();
                            if (ab == "Y" || ab == "N")
                            {
                                if (ab == "Y")
                                {
                                    dr.AdditionalBed = true;
                                }
                                else
                                {
                                    dr.AdditionalBed = false;
                                }
                                break;
                            }
                            else
                            {
                                Console.WriteLine("Invalid input.");
                            }
                        }
                        s.AddRoom(dr);
                    }
                }
                ri++;
            }
        }
        while (true)
        {
            Console.Write("Select another room[Y/N]: ");
            string? ar = Console.ReadLine();
            if (ar == "Y" || ar == "N")
            {
                if (ar == "N")
                {
                    anotherroom = false;
                }
                break;
            }
            else
            {
                Console.WriteLine("Invalid input.");
            }

        }
        if (anotherroom == false)
        {
            break;
        }
    }
    choice -= 1;
    int gi = 0;
    foreach (Guest g in gList)
    {
        if (choice == gi)
        {
            g.HotelStay = s;
            g.IsCheckedin = true;
            break;
        }
        gi++;
    }
    Console.WriteLine("Guest check in successfully: ");
}

void GuestStaydetails(List<Guest> gList, int num)
{
    int choice = 0;
    while (true)
    {
        Console.Write("Enter your option: ");
        try
        {
            choice = Convert.ToInt32(Console.ReadLine());
            if (choice >= 1 && choice <= (num - 1))
            {
                break;
            }
            else
            {
                Console.WriteLine("Invalid option");
            }
        }
        catch (System.FormatException)
        {
            Console.WriteLine("Invalid option");
        }
    }
    choice -= 1;
    int gi = 0;
    foreach (Guest g in gList)
    {
        if (choice == gi)
        {
            //Check if got stay detail b4 printing
            if (g.HotelStay == null)
            {
                Console.WriteLine("No stay details!");
            }
            else
            {
                Console.WriteLine(g.HotelStay.ToString());
                break;
            }
        }
        gi++;
    }
}

void ExtendStay(List<Guest> gList, int num)
{
    int choice = 0;
    while (true)
    {
        Console.Write("Enter your option: ");
        try
        {
            choice = Convert.ToInt32(Console.ReadLine());
            if (choice >= 1 && choice <= (num - 1))
            {
                break;
            }
            else
            {
                Console.WriteLine("Invalid option");
            }
        }
        catch (System.FormatException)
        {
            Console.WriteLine("Invalid option");
        }
    }
    choice -= 1;
    int gi = 0;
    foreach (Guest g in gList)
    {
        if (choice == gi && g.IsCheckedin == true)
        {
            int numday = 0;
            while (true)
            {
                Console.Write("Enter number of days to extend: ");
                try
                {
                    numday = Convert.ToInt32(Console.ReadLine());
                    if (numday > 0)
                    {
                        break;
                    }
                    else
                    {
                        Console.WriteLine("Invalid input");
                    }
                }
                catch (System.FormatException)
                {
                    Console.WriteLine("Invalid input");
                }
            }
            g.HotelStay.CheckOutDate = g.HotelStay.CheckOutDate.AddDays(numday);
            Console.WriteLine("Updated successfully");
            break;
        }
        if (choice == gi && g.IsCheckedin == false)
        {
            Console.WriteLine("Unable to extend as you are not check in.");
            break;
        }
        gi++;
    }
}

void CheckOut(List<Guest> gList, List<Room> rList, int num)
{
    int choice = 0;
    while (true)
    {
        Console.Write("Enter your option: ");
        try
        {
            choice = Convert.ToInt32(Console.ReadLine());
            if (choice >= 1 && choice <= (num - 1))
            {
                break;
            }
            else
            {
                Console.WriteLine("Invalid option");
            }
        }
        catch (System.FormatException)
        {
            Console.WriteLine("Invalid option");
        }
    }
    choice -= 1;
    int gnum = 0;
    foreach (Guest g in gList)
    {
        if (gnum == choice && g.IsCheckedin == true)
        {
            double TotBill = g.HotelStay.CalculateTotal();
            Console.WriteLine("Total Bills: $" + TotBill.ToString("0.00"));
            Console.WriteLine(g.Member.ToString());
            if (g.Member.Status != "Ordinary")
            {
                while (true)
                {
                    Console.Write("Do you want to use" +
                    " points to offset total bill[Y/N]: ");
                    string? option = Console.ReadLine();
                    if (option == "Y" || option == "N")
                    {
                        if (option == "Y")
                        {
                            while (true)
                            {
                                try
                                {
                                    Console.Write("Number of points " +
                                    "to offset total bill payment: ");
                                    int point = Convert.ToInt32(Console.ReadLine());
                                    bool success = g.Member.RedeemPoints(point);
                                    if (success)
                                    {
                                        TotBill = TotBill - Convert.ToDouble(point);
                                        Console.WriteLine("Total Bills: $" + TotBill.ToString("0.00"));
                                        Console.Write("Press any key to make payment");
                                        string? input = Console.ReadLine();
                                        g.IsCheckedin = false;
                                        g.Member.EarnPoints(TotBill);
                                        break;
                                    }
                                }
                                catch (System.FormatException)
                                {
                                    Console.WriteLine("Invalid option");
                                }
                            }
                        }
                        else
                        {
                            Console.Write("Press any key to make payment");
                            string? input = Console.ReadLine();
                            g.IsCheckedin = false;
                            g.Member.EarnPoints(TotBill);
                        }
                        
                        break;
                    }
                    else
                    {
                        Console.WriteLine("Invalid input.");
                    }
                }
                
            }
            else
            {
                Console.Write("Press any key to make payment");
                string? input = Console.ReadLine();
                g.IsCheckedin = false;
                g.Member.EarnPoints(TotBill);
            }
            foreach (Room r in g.HotelStay.RoomList)
            {
                foreach(Room allr in rList)
                {
                    if (r.RoomNumber == allr.RoomNumber)
                    {
                        r.IsAvail = true;
                        allr.IsAvail = true;
                        break;
                    }
                    
                }
                
            }
            break;
        }
        else if (gnum == choice && g.IsCheckedin == false)
        {
            Console.WriteLine("Guest not checked in");
            break;
        }
         gnum++;
    }
}

List<string> InitmList()
{
    List<string> mList = new List<string>();
    mList.Add("Jan");
    mList.Add("Feb");
    mList.Add("Mar");
    mList.Add("Apr");
    mList.Add("May");
    mList.Add("Jun");
    mList.Add("Jul");
    mList.Add("Aug");
    mList.Add("Sep");
    mList.Add("Oct");
    mList.Add("Nov");
    mList.Add("Dec");
    return mList;
}

List<double> InitmaList()
{
    List<double> maList = new List<double>();
    for (int i = 1; i < 13; i++)
    {
        maList.Add(0.00);
    }
    return maList;
}
void Calyear(List<Guest> gList, List<string> mList, List<double> maList)
{
    int year = 0;
    double mtotal = 0;
    double ytotal = 0;
    while (true)
    {
        Console.Write("Enter the year: ");
        try
        {
            year = Convert.ToInt32(Console.ReadLine());
            if (year >= 2000 && year <= DateTime.Now.Year) 
            {
                break;
            }
            else
            {
                Console.WriteLine("Invalid year input!");
            }
        }
        catch (System.FormatException)
        {
            Console.WriteLine("Invalid option");
        }
    }
    foreach (Guest g in gList)
    {
        if (g.HotelStay != null)
        {
            if (g.HotelStay.CheckOutDate.Year == year)
            {
                for (int i = 1; i < 13; i++)
                {

                    if (g.HotelStay.CheckOutDate.Month == i)
                    {
                        mtotal = g.HotelStay.CalculateTotal();
                        maList[i - 1] += mtotal;
                    }
                }
            }
        }
        
    }
    double tempmtotal = 0;
    for (int j = 0; j < maList.Count; j++)
    {
        tempmtotal = maList[j];
        Console.WriteLine(mList[j] + " " + year + ": $" +
            tempmtotal.ToString("0.00"));
        ytotal += maList[j];
    }
    Console.WriteLine("Total: $" + ytotal.ToString("0.00"));
}
