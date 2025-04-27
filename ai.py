import discord
from discord.ext import commands
import os
from model import get_class

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)  # Klasör yoksa oluştur
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def sa(ctx):
    await ctx.send(f'as {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)


@bot.command()
async def check(ctx):
    # Mesajın ekli bir dosya içerip içermediğini kontrol ediyoruz
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:  # Mesajdaki tüm ekleri döngüyle kontrol ediyoruz
            file_name = attachment.filename  # Dosya adını alıyoruz
            

            # Dosyanın kaydedileceği yolu oluşturuyoruz
            file_path = os.path.join(IMAGE_DIR, file_name)

            try:
                await attachment.save(file_path)  # Dosyayı belirtilen klasöre kaydediyoruz
                await ctx.send(f"✅ Görsel başarıyla kaydedildi: `{file_path}`")  # Kullanıcıya başarı mesajı gönderiyoruz

                model_path= "keras_model.h5"
                labels_path="labels.txt"
                class_name, confidence = get_class(file_path, model_path, labels_path)

                messages = {
    "masaustu": "Bu bir masaüstü bilgisayardır. Genellikle sabit bir yerde kullanılır ve güçlü donanımlara sahiptir.",
    "laptop": "Bu bir dizüstü bilgisayardır. Taşınabilirliği sayesinde iş ve eğitim için sıkça tercih edilir.",
    "tablet": "Bu bir tablettir. Dokunmatik ekranı ile genellikle eğlence ve hafif işler için kullanılır.",
    "telefon": "Bu bir akıllı telefondur. İletişim, internet ve mobil uygulamalar için idealdir."
}
                

                # class_name'in küçük harf olup olmadığını kontrol et
            
                special_message = messages.get(class_name,"bu sözlükte yok")
            
                await ctx.send(f"🔍 Tahmin: {class_name[2:]} (%{confidence*100:.2f} güven) {special_message}")
            except Exception as e:
                await ctx.send(f"⚠ Hata oluştu: {str(e)}")


            except Exception as e:  # Eğer bir hata oluşursa
                await ctx.send(f"⚠️ Görsel kaydedilirken hata oluştu: {str(e)}")  # Kullanıcıya hata mesajı gönderiyoruz
    else:
        await ctx.send("⚠️ Görsel yüklemeyi unuttun!")  # Kullanıcıya görsel yüklemesi gerektiğini hatırlatıyoruz



bot.run("MTMwNzcxNjQxNzEyMjA3ODgwMQ.G67o8i.x5NEhUjIOMdjRSkjIKT2gQbcbU1wn1InZtKPHk") 