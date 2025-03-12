Welcome to NetBruter!

  This program initially started as a project to test the ability to generate theoretical IPs and scan them. After realizing that I could indeed create such IPs, I implemented threading to scan thousands of IPs in just seconds. Once an active IP is found, the program utilizes the ipinfo.io API to retrieve geolocation information.

  Following this, the program automatically attempts to brute-force open ports to discover valid credentials. Please note that this tool is still under development, and there is a high likelihood of encountering false positives.

To assist you in identifying valid results, be sure to review:

  The verbose output that provides detailed server responses.
  The Discord webhook notification (which you can enable by configuring line 776).

Looking Ahead:

  I’m currently working on a second version of this program to rewrite it in a more clean, modular, and readable way. When I first created this script, I was new to using classes, so the code is not the cleanest. Additionally, the way the program was originally built makes it difficult to add new features and enhancements.

  That said, I welcome any and all help to improve this script. Any suggestions, contributions, or feedback are greatly appreciated to help make it cleaner, more efficient, and feature-rich.

