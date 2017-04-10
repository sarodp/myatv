# myatv
My TV test pattern generator


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
 
ปุ่มกด  
 GPIO.23 [pin16] = swUP = up image เดินหน้าภาพ
 GPIO.24 [pin18] = swUP = down image ถอยหลังภาพ
 GPIO.25 [pin22] = swRND = random image สุ่มภาพ สลับทุก 1 วินาที 
 
rc.local 
$ sudo geany /etc/rc.local  
..แทรกคำสั่งนี้ ก่อนจบไฟล์ตามตย.  เพื่อรันแบบออโต้บู้ท
  python /home/pi/myatv/myatv.py > /dev/null
  exit 0        

config.txt
$ sudo geany /boot/config.txt
..แก้ไขไฟล์นี ้เพื่อปรับเอาท์พุท ให้พอดีกับสัญญาณภาพจอทีวี
