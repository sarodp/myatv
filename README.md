# myatv
  My TV test pattern generator  
  
  
CREDITS:  
 (c) pa3bwe, pa3bwe@amsat.org  
 this program maybe freely used and distributed for amateur (ham) purposes  
 a qsl card is appreciated!   
SOURCES:  
  atv2.py -sound added  
  atv3.py -added possibility to use switch to scroll through images  
             two switches connected to header pin 24+26 (GPIO8 + GPIO7) and gnd  
 		      see http://tinyurl.com/6wq9l86  
		      added cmd line call to amixer to increase sound level  
  tstptn00.py -another source   
   
---  
    
ตัวอย่างโปรแกรม Pygame บนราสเบอรีี่ไพ  
ปรับแต่งจากโปรแกรม atv3.py ตามลิงค์ข้างต้น   
สร้างเป็นเครื่องกำเนิดสัญญาณภาพทดสอบหน้าจอทีวี   
..อินพุทรับค่าอินเตอร์รัพท์จาก GPIO23,24,25 (pin 16,18,22)  
..เป็นแบบ negative edge trig พร้อมตั้งค่า debounce ได้ด้วย  
..อินพุทจากคีย์บอร์ดได้ด้วย  
..รันอัตโนมัติแบบ headless โดยแก้ไขไฟล์ /etc/rc.local ตามตย.  
..เอาท์พุทเป็นสัญญาณออกจอทีวี กำหนดด้วยไฟล์ /boot/config.txt ตามตย.  
  
---  
## วิธีติดตั้งและทดสอบโปรแกรมเบื้องต้น  
$ cd ~  
$ git clone https://github.com/sarodp/myatv.git  
...  
  
$ cd myatv  
$ sudo python myatv.py  
...  

คีย์บอร์ด  
 [F1]..[F12] = load image01.jpg ... image12.jpg  
 [s] = sound off ปิดเสียง  
 [r] = random imagexx.jpg สุ่มภาพ สลับทุก 1 วินาที   
 [Esc] = quit ออกโปรแกรม
   
ปุ่มกด    
 GPIO.23 [pin16] = swUP = up image เดินหน้าภาพ  
 GPIO.24 [pin18] = swUP = down image ถอยหลังภาพ  
 GPIO.25 [pin22] = swRND = random image สุ่มภาพ สลับทุก 1 วินาที   
  
## แก้ไขสองไฟล์นี้ เมื่อนำไปใช้งานแบบ headless pi  
rc.local   
$ sudo geany /etc/rc.local    
..แทรกคำสั่งนี้ ก่อนจบไฟล์ตามตย.  เพื่อรันแบบออโต้บู้ท  
  python /home/pi/myatv/myatv.py > /dev/null  
  exit 0         
  
config.txt  
$ sudo geany /boot/config.txt  
..แก้ไขไฟล์นี ้เพื่อปรับเอาท์พุท ให้พอดีกับสัญญาณภาพจอทีวี  
