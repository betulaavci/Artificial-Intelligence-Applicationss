# 1) Aşağıdaki sözlükte, değerler içinde c harfinin geçip geçmediğini gösteren bir if koşulu yazınız

my_dictionary = {"k1":10,"k2k":"a","k32":30,"k4":"c"}
if any("c" in str(deger) for deger in my_dictionary.values()):
    print("Sözlükteki değerler içinde 'c' harfi geçiyor.")
else:
    print("Sözlükteki değerler içinde 'c' harfi geçmiyor.")

# 2) Aşağıdaki listedeki sayılardan sadece çift sayı olanları başka bir listeye kaydeden bir kod yazınız.

my_numbers = [1,2,3,4,5,6,19,20,32,21,20,1111,23,24]
cift = []
for i in my_numbers:
    if i % 2 == 0 :
       cift.append(i)
print(cift)

# 3) Tüm dairelerin çevresini içeren başka yeni bir liste oluşturunuz. (İpucu: 2 * pi * r)  Pi 3.14 alınabilir.

r_list = [3,2,5,8,4,6,9,12]
pi = 3.14
cevrehesapla = []
for i in r_list:
    cevre = 2 * pi * i
    cevrehesapla.append(cevre)
print(cevrehesapla)

# 4) Aşağıdaki listede isim - yaş eşleşmelerinin bulunduğu yapılar mevcuttur. Sadece yaşların olduğu yeni ve ayrı bir liste oluşturunuz.

age_name_list = [("Ahmet",30),("Ayse",24),("Mehmet",40),("Fatma",29)]
yeni_list = []

for i in age_name_list :
    yeni_list.append(i[1])
print(yeni_list)


# 5) Aşağıdaki müzik gruplarından birini rastgele yazdıran bir kod yazınız
import random

metal_list = ["Metallica","Iron Maiden","Dream Theater","Megadeth","AC/DC"]

muzik = random.choice(metal_list)
print(muzik)


# 6) Aşağıdaki kodun çıktısı ne olacaktır?

number_list = [5,7,18,21,20,10,405,24]
print(number_list)
print([num % 2 == 0 for num in number_list])

#7) Aşağıdaki string dizisinde, içinde sadece XYZ geçen barkodları gösterecek yeni bir liste oluşturunuz

barcodeList = ["ABC231","SA3123XYZ","XYZA123Q","QRE1231KJ","X112QGL"]

if any("XYZ" in str(deger) for deger in barcodeList):
    print("Sözlükteki değerler içinde 'XYZ' harfi geçiyor.")
else:
    print("Sözlükteki değerler içinde 'XYZ' harfi geçmiyor.")

#8) Aşağıda yazdırılan sınıfı incelediğinizde my_cat.multiply_age() kodunun çıktısı ne olacaktır?


class Cat:
    def __init__(self, name, age=5):
        self.name = name
        self.age = age

    def multiply_age(self):
        return self.age * 3

my_cat = Cat("Whiskers")
print(my_cat.multiply_age())

metal_list = ["Metallica","Iron Maiden","Dream Theater","Megadeth","AC/DC"]
from random import randint
print(metal_list[randint(0,len(metal_list)-1)])
