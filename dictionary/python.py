import json
import os
 
def load_config():
    
    default_languages = ["Türkçe", "İngilizce", "Fransızca"]
    try:
        if not os.path.exists("config.json"):
        # Varsayılan dilleri içeren bir config.json dosyası oluştur
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump({"languages": default_languages}, f, ensure_ascii=False, indent=4)
 
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            return config["languages"]
    except json.JSONDecodeError:
        print("config.json dosyası hatalı!")
        return default_languages
 
def save_config(languages):
    
    try:
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump({"languages": languages}, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Dil konfigürasyonu kaydedilirken bir hata oluştu: {e}")
 
def load_words():
    #Kelimeleri yükler
    try:
        if not os.path.exists("words.json"):
            # Eğer words.json yoksa boş bir dosya oluştur
            with open("words.json", "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
 
        with open("words.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("words.json dosyası hatalı!")
        return []
 
def save_words(word_list):
    #Kelimeleri kaydeder
    try:
        with open("words.json", "w", encoding="utf-8") as f:
            json.dump(word_list, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Kelimeler kaydedilirken bir hata oluştu: {e}")
 
def select_language(languages, prompt):
    #Kullanıcıdan dil seçimini alır
    while True:
        print("\nMevcut diller:")
        for i, lang in enumerate(languages, 1):
            print(f"{i}. {lang}")
 
        try:
            choice = int(input(f"\n{prompt} (1-{len(languages)}): "))
            if 1 <= choice <= len(languages):
                return languages[choice - 1]
            else:
                print("Lütfen geçerli bir sayı giriniz!")
        except ValueError:
            print("Lütfen geçerli bir sayı giriniz!")
 
def search_word(word_list, source_lang, target_lang, search_term):
        #Kelime araması yapar
        # Kullanıcıdan gelen kelimeyi küçük harfe dönüştür ve boşlukları temizle
    search_term_lower = search_term.strip().lower()
 
    for word_entry in word_list:
        # Kaydedilen kelimeleri küçük harfe dönüştürerek karşılaştırma yap
        source_word = word_entry.get(source_lang, "").lower()
 
        if source_word == search_term_lower:
            return word_entry.get(target_lang, None)
    return None
 
def get_valid_answer(prompt):
        #Geçerli 'evet' veya 'hayır' cevabını almak için fonksiyon
    while True:
        answer = input(prompt).strip()
        # Yalnızca küçük harfli 'evet' veya 'hayır' kabul edilir
        if answer == "evet" or answer == "hayır":
            return answer
        else:
            print("Lütfen 'evet' veya 'hayır' olarak cevap verin.")
 
def main():
    # Konfigürasyonu yükle
    languages = load_config()
 
    # Kelimeleri yükle
    word_list = load_words()
 
    source_lang = None
    target_lang = None
 
    while True:
        print("\n=== SÖZLÜK PROGRAMI ===")
        print("1. Dil Ayarları")
        print("2. Kelime Ara")
        print("3. Çıkış")
 
        try:
            choice = int(input("Seçiminiz (1-3): "))
 
            if choice == 1:
                # Dil seçimi
                while True:
                    source_lang = select_language(languages, "Başlangıç dilini seçin")
                    target_lang = select_language(languages, "Hedef dili seçin")
 
                    if source_lang == target_lang:
                        print("\nBaşlangıç ve hedef dili aynı seçemezsiniz!")
                        retry = get_valid_answer("Dil seçimini tekrar yapmak ister misiniz? (evet/hayır): ")
 
                        if retry == "hayır":
                            source_lang = None
                            target_lang = None
                            break  # Ana menüye dön
                        elif retry == "evet":
                            continue  # Başlangıç ve hedef dili baştan seçtir
 
                    else:
                        print(f"\nBaşlangıç dili: {source_lang}")
                        print(f"Hedef dil: {target_lang}")
                        # Kelime aramak isteyip istemediğini sor
                        while True:
                            search_choice = get_valid_answer("\nKelime aramak ister misiniz? (evet/hayır): ")
                            if search_choice == "evet":
                                search_term = input("\nAramak istediğiniz kelimeyi girin: ")
                                result = search_word(word_list, source_lang, target_lang, search_term)
 
                                if result:
                                    print(f"\nSonuç bulundu: {search_term} -> {result}")
                                else:
                                    print("\nSonuç bulunamadı!")
                            elif search_choice == "hayır":
                                break  # Ana menüye dön
                        break  # Dil seçimi sonrası menüye dön
 
            elif choice == 2:
                # Kelime arama
                if not source_lang or not target_lang:
                    print("\nLütfen önce dil ayarlarını yapın!")
                    continue
 
                while True:
                    search_term = input("\nAramak istediğiniz kelimeyi girin: ")
                    result = search_word(word_list, source_lang, target_lang, search_term)
 
                    if result:
                        print(f"\nSonuç bulundu: {search_term} -> {result}")
                    else:
                        print("\nSonuç bulunamadı!")
 
                    # Tekrar kelime aramak isteyip istemediğini sor
                    search_again = get_valid_answer("\nBaşka bir kelime aramak ister misiniz? (evet/hayır): ")
                    if search_again != "evet":
                        break  # Ana menüye dön
 
            elif choice == 3:
                print("\nProgram sonlandırılıyor...")
                break
 
            else:
                print("\nLütfen geçerli bir seçim yapın!")
 
        except ValueError:
            print("\nLütfen geçerli bir sayı girin!")
 
if __name__ == "__main__":
    main()