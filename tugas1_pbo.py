# class untuk item senjata
class Item:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

# class untuk hero
class Hero:
    def __init__(self, name, attack_power):
        self.name = name
        self.attack_power = attack_power
        self.hp = 300
        self.item = None # set none di awal sblm pasang item

    # method untuk masang item
    def set_item(self, item):
        # cek dulu biar slot item ga ketimpa
        if self.item is not None:
            print(f"{self.name} sudah memiliki senjata.")
        else:
            self.item = item
            print(f"{self.name} berhasil memakai {item.name} !")

    # memotong hp hero dan cegah minus
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        print(f"HP {self.name} sekarang {self.hp}")

    # method bawaan untuk menyerang
    def attack(self, enemy):
        # damage awal ambil dr base hero
        total_damage = self.attack_power
        nama_senjata = "Tangan Kosong"
        
        # tambah damage kalo pake senjata
        if self.item is not None:
            total_damage += self.item.damage
            nama_senjata = self.item.name
            
        print(f"{self.name} menyerang {enemy.name} dengan senjata {nama_senjata} sebesar {total_damage}")
        
        # panggil method musuh (polymorphism)
        enemy.take_damage(total_damage, self)


# parent class musuh
class Enemy:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    # method kosong buat dioverride
    def take_damage(self, damage, hero):
        pass

# musuh biasa tanpa shield
class BasicEnemy(Enemy):
    # terima damage murni
    def take_damage(self, damage, hero):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
            
        print(f"HP {self.name} sekarang {self.hp}")

# musuh pakai shield 30
class ShieldEnemy(Enemy):
    def __init__(self, name, hp):
        super().__init__(name, hp)
        self.shield = 30

    def take_damage(self, damage, hero):
        # potong damage base pakai shield 30
        damage_akhir = damage - self.shield
        
        # cegah minus biar ga nambah hp
        if damage_akhir < 0:
            damage_akhir = 0
            
        print(f"{self.name} mengaktifkan shield!\nDamage berkurang menjadi {damage_akhir}")
        
        self.hp -= damage_akhir
        if self.hp < 0:
            self.hp = 0
            
        print(f"HP {self.name} sekarang {self.hp}")

# bos musuh (shield 40, attack 50)
class BossEnemy(Enemy):
    def __init__(self, name, hp):
        super().__init__(name, hp)
        self.shield = 40
        self.attack_power = 50

    def take_damage(self, damage, hero):
        damage_akhir = damage - self.shield
        if damage_akhir < 0:
            damage_akhir = 0
            
        print(f"{self.name} mengaktifkan shield!\nDamage berkurang menjadi {damage_akhir}")
        
        self.hp -= damage_akhir
        if self.hp < 0:
            self.hp = 0
            
        print(f"HP {self.name} sekarang {self.hp}")
        
        # bos otomatis counter kalo msh hidup
        if self.hp > 0:
            print(f"{self.name} menyerang balik {hero.name} sebesar {self.attack_power}")
            hero.take_damage(self.attack_power)


# class utama pembungkus alur program
class Game:
    def __init__(self):
        # nampung array hero dan item
        self.heroes = []
        self.items = {}

    # nambahin hero ke dalem list
    def add_hero(self, hero):
        self.heroes.append(hero)

    # nambahin item ke dict
    def add_item(self, item):
        self.items[item.name] = item

    # ngambil object hero klo cocok
    def find_hero(self, name):
        for hero in self.heroes:
            if hero.name == name:
                return hero
        return None

    # ngambil object item klo ada namanya
    def find_item(self, name):
        if name in self.items:
            return self.items[name]
        return None

    # boolean ngecek klo smua hero dh punya item
    def all_have_items(self):
        for hero in self.heroes:
            if hero.item is None:
                return False
        return True

    # nge-wrap mekanisme pasang perlengkapan senjata
    def prepare_items(self):
        print("=== PASANG SENJATA ===")
        while True:
            command = input("Command (PASANG;Hero;Item / DONE): ")
            if command == "DONE":
                break
                
            parts = command.split(";")
            if parts[0] == "PASANG":
                nama_h = parts[1]
                nama_i = parts[2]
                
                # manggil func dari di atas buat narik datanya
                hero_target = self.find_hero(nama_h)
                item_target = self.find_item(nama_i)

                # # logika error message
                # if hero_target is None:
                #     print(f"Peringatan: Hero '{nama_h}' tidak ditemukan di daftar!")
                # elif item_target is None:
                #     print(f"Peringatan: Senjata '{nama_i}' tidak ditemukan di daftar!")
                # else:
                #     # Kalo dua-duanya aman (tidak None), baru pasang senjatanya
                #     hero_target.set_item(item_target)
                
                # cek kalo objek beneran ketemu sblm di-set
                if hero_target is not None and item_target is not None:
                    hero_target.set_item(item_target)

    def main(self):
        # loop masukin data hero
        jumlah_hero = int(input("Masukkan jumlah hero: "))
        for i in range(jumlah_hero):
            data_hero = input(f"Hero {i+1} (format: Nama%Attack): ")
            parts = data_hero.split("%")
            # panggil abstraksinya buat masang
            hero_baru = Hero(parts[0], int(parts[1]))
            self.add_hero(hero_baru)

        # loop masukin data item
        jumlah_item = int(input("Masukkan jumlah item: "))
        for i in range(jumlah_item):
            data_item = input(f"Item {i+1} (format: Nama;Damage): ")
            parts = data_item.split(";")
            # simpen pake add item
            item_baru = Item(parts[0], int(parts[1]))
            self.add_item(item_baru)

        # panggil perulangan persiapannya dsni
        self.prepare_items()

        # mulai battle level 1
        print("=== LEVEL 1 ===")
        data_enemy = input("Enemy Level 1 (format: Nama*HP): ")
        parts = data_enemy.split("*")
        enemy_1 = BasicEnemy(parts[0], int(parts[1]))
        self.battle(enemy_1)

        print()

        # lanjut battle level 2
        print("=== LEVEL 2 ===")
        data_enemy = input("Enemy Level 2 (format: Nama*HP): ")
        parts = data_enemy.split("*")
        enemy_2 = ShieldEnemy(parts[0], int(parts[1]))
        self.battle(enemy_2)

        print()

        # babak akhir lawan bos
        print("=== LEVEL 3 ===")
        data_enemy = input("Enemy Level 3 (format: Nama*HP): ")
        parts = data_enemy.split("*")
        enemy_3 = BossEnemy(parts[0], int(parts[1]))
        self.battle(enemy_3)

    # logika turn masing-masing hero
    def battle(self, enemy):
        print("=== MULAI MENYERANG ===")
        for hero in self.heroes:
            # stop kalo musuh udh keburu kalah
            if enemy.hp <= 0:
                break
            
            # trigger hero untuk attack musuh
            hero.attack(enemy)
            
            # cek sisa hp musuh paska dipukul
            if enemy.hp == 0:
                print(f"{enemy.name} berhasil dikalahkan!")
                break
                
        # info sisa hp akhir kalo blm beres
        if enemy.hp > 0:
            print(f"{enemy.name} masih hidup dengan HP {enemy.hp}")

# dijalanin dari sini
if __name__ == "__main__":
    game = Game()
    game.main()
