# Simulations
## Giriş

Marsyard paketi için blender_gazebo adında bir paket lazımdır fakat bu başka bir repodan submodule olarak çekilmektedir o yüzden bu repo aşagodaki kod ile workspace'e clonelanmalı.

```
git clone --recurse-submodules https://github.com/itu-rover/Simulations.git
```

Bu repo temelde 2 tür simülasyon barındırmaktadır rover_21_descriptions sadece Alt yürüleri içermekte ve 3 tip araç bulunmaktadır bunlar:
- ZED'li alt yürür
- D435'lü yürür
- Velodyne Lidarlı yürür

--------------------------------------------------------------------------------------------------------------------------
## IMU ve GPS gibi verilerin alınması
Bu verilerin alınması için kurulması gerek paketler aşağıda komut konsola girildiği zaman kurulacaktır.

```
sudo apt install ros-melodic-hector-gazebo-*
```

-----------------------------------------------------------------------------------------------------------------
rover_21_robotic_arm ise alt yürürle beraber robot kol içermektedir. burada kol üstünde 2 fpv kamera bir tane d435 bulunmaktadır.

## rover_21_robotic_arm'ın çalıştırılması
Simülasyonu çalıştırmak için öncellikle şu eklenili paketlere ihtiyacnız var 
1. `sudo apt install ros-melodic-twist-mux`
2. `sudo apt install ros-melodic-multimaster-launch`
3. `sudo apt install ros-melodic-joy`

bunlardan birinci paket realsense için ikinci ise alt yürürü joystik olmadan hareket ettirmek için gerekli. Bunlar yüklendikten sonra `catkin build` yapılır daha sonra `source devel/setup.bash` yapılır.

Gerekli Launch dosyaları:

Gazebo, Rviz, Alt yürür ve Robot kol kontrolcüleri için

`roslaunch arm_21_gazebo arm_gazebo.launch`

İsterseniz kontrolcüleri test etmek için yani robot kolu ileri kinematikle ve alt yürürü joystick ile elle sürmek isterseniz ayryetten mod switch algortimasına bakmak isterseniz şu dosya çalıştırlacak. Python kodu ise robot_drive paketi içinde src klasörü altındaki forward_kinematic klasörünün altında bulunan forward_kinematic.py'dır. NOT: En yakın zamanda bu kod daha güzel bir şekilde C++'a geçirilecektir. 

`roslaunch robot_drive kinematic.launch`

Robot Kol sürüş: Sağ, Sol analog ve ok tuşları

Alt Yürür Sürüş: R1 basılı tutarak Turbo mod L1 basılı tutarak normal mod sürüşün kontrolü ise sol analog

Mod Switch: R2'ye bir kez basarak gerçekleşir simülasyon ilk açıldığında Robot kol sürüşü açıktır R2'ye basıldığında alt yürüre geçer. Dilerseniz R2 ye basarak tekrar robot kola geçebilirsiniz.

--------------------------------------------------------------------------------------------------------------------------
## rover_21_descriptions içindeki paketlerin çalıştırılması
--------------------------------------------------------------------------------------------------------------------------

D435'li simülasyonun çalıştırılması için repo klonlandıktan sonra `catkin build` yapılır sonra `source devel/setup.bash` yapılır.

Sadece Gazebo için:

`roslaunch rover_21_description_d435 gazebo.launch`

Sadece Rviz için:

`roslaunch rover_21_description_d435 d435_rviz.launch`

Hem Rviz Hem Gazebo için:

`roslaunch rover_21_description_d435 rviz_and_gazebo.launch`

çalıştırılmalıdır eğer Rviz configurasyonu değiştirlip kaydedilmek istenirse ilgili paketin içinde yer alan rviz klasörüne "urdf.rviz" adıyla rviz konfigürasyonu kaydedilebilir. 

------------------------------------------------------------------------------------------------------------------------------------------

ZED'li simulasyon için test edildiği kadarıyla herhangi ek paket kulmasına gerek yoktur ancak ZED kamera ile test yapılacaksa şu linkten ZED'in ros wraper'nın kurulması önerilir. [https://github.com/stereolabs/zed-ros-wrapper.git](https://github.com/stereolabs/zed-ros-wrapper.git)

Sadece Gazebo için:

`roslaunch rover_21_description_zed gazebo.launch`

Sadece Rviz için:

`roslaunch rover_21_description_zed zed_rviz.launch`

Hem Rviz Hem Gazebo için:

`roslaunch rover_21_description_zed rviz_and_gazebo.launch`

çalıştırılmalıdır rviz konfigurasyonu kayıt işi d435 simülasyonu ile aynıdır.

----------------------------------------------------------------------------------------------------------------------------------------------
Velodyne'lı paket için repo klonlandıktan sonra `catkin build` yapılmalı sonrasında `source devel/setup.bash` yapıldıktan sonra.

Sadece Gazebo için:

`roslaunch rover_21_description_velodyne gazebo.launch`

Sadece Rviz için:

`roslaunch rover_21_description_velodyne velodyne_rviz.launch`

Hem Rviz Hem Gazebo için:

`roslaunch rover_21_description_velodyne rviz_and_gazebo.launch`

-----------------------------------------------------------------------------------------------
## marsyard
-----------------------------------------------------------------------------------------------
Marsyard paketi için blender_gazebo adında bir paket lazımdır fakat bu başka bir repodan submodule olarak çekilmektedir o yüzden bu repo aşagıdaki kod ile workspace'e clonelanmalı.

```
git clone --recurse-submodules https://github.com/itu-rover/Simulations.git
```

NOT: bu paketin içindeki launch dosyaları simülasyon dosyaları tarafından otomatik çağırlmakta bu pakette değişliklik yapmanıza gerek olmayacaktır. Ancak bir sebepten ötürü harita değiştirmek isterseniz gazebo.launch veya arm_gazebo.launch dosyalarını editleyebilirsiniz.

NOT 2: Eğer performans sıkıntı yaşarsanız haritalarda bana ulaşın.

NOT 3: GIT LFS ile dae pushlayamama sorunu çözülmüştür.

------------------------------------------------------------------------------------------
## ArTagler
------------------------------------------------------------------------------------------
Alt Yürürlü haritalar için Artaglar eklenmiştir.

TODO: Artag Konumları haritada biraz daha düzenlenecek ileriki commitlerde bu duruma bakılacak.