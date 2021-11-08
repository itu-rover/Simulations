# Simulations
## Giriş 
Bu repo temelde 2 tür simülasyon barındırmaktadır rover_21_descriptions sadece Alt yürüleri içermekte ve 3 tip araç bulunmaktadır bunlar:
- ZED'li alt yürür
- D435'lü yürür
- Velodyne Lidarlı yürür

--------------------------------------------------------------------------------------------------------------------------

rover_21_robotic_arm ise alt yürürle beraber robot kol içermektedir. burada kol üstünde 2 fpv kamera bir tane d435 bulunmaktadır.

## rover_21_robotic_arm'ın çalıştırılması
Simülasyonu çalıştırmak için öncellikle şu eklenili paketlere ihtiyacnız var 
1. [https://github.com/issaiass/realsense_gazebo_plugin.git](https://github.com/issaiass/realsense_gazebo_plugin.git)
2. [https://github.com/ros-visualization/interactive_marker_twist_server.git](https://github.com/ros-visualization/interactive_marker_twist_server.git)
3. `sudo apt install ros-melodic-twist-mux`
4. `sudo apt install ros-melodic-multimaster-launch`
5. `sudo apt install ros-melodic-joy`

bunlardan birinci paket realsense için ikinci ise alt yürürü joystik olmadan hareket ettirmek için gerekli. Bunlar yüklendikten sonra `catkin_make` yapılır daha sonra `source devel/setup.bash` yapılır.

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

D435'li simülasyonu çalıştırmak bu simülasyonun çalıştırılması için workspace' ayrı olarak realsense gazebo plugin'i eklenmeli [https://github.com/issaiass/realsense_gazebo_plugin.git](https://github.com/issaiass/realsense_gazebo_plugin.git) ve `catkin_make` yapıldıktan sonra `source devel/setup.bash` yapılmalı. sonra

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
Velodyne'lı paket içinse öncelikle şu repodan [https://bitbucket.org/DataspeedInc/velodyne_simulator.git](https://bitbucket.org/DataspeedInc/velodyne_simulator.git) **velodyne_gazebo_plugins** paketi src klasörüne indirilmeli. Ardından `catkin_make` yapılmalı sonrasında `source devel/setup.bash` yapıldıktan sonra.

Gazebo için:

`roslaunch rover_21_description_velodyne gazebo.launch`

Sadece Rviz için:

`roslaunch rover_21_description_velodyne velodyne_rviz.launch`

Hem Rviz Hem Gazebo için:

`roslaunch rover_21_description_velodyne rviz_and_gazebo.launch`

-----------------------------------------------------------------------------------------------
## marsyard
-----------------------------------------------------------------------------------------------
Bu paket araçların spawnlanacağı mars yüzeyini içermekte be bunun çalıştırılması için ek bir pakete ihtiyaç vardır önce onu kurunuz.
[https://github.com/david0429/blender_gazebo.git](https://github.com/david0429/blender_gazebo.git) bu paket kurulduktan sonra marsyardı kullanabilirsiniz.

NOT: bu paketin içindeki launch dosyaları simülasyon dosyaları tarafından otomatik çağırlmakta bu pakette değişliklik yapmanıza gerek olmayacaktır. Ancak bir sebepten ötürü harita değiştirmek isterseniz gazebo.launch veya arm_gazebo.launch dosyalarını editleyebilirsiniz.

NOT 2: Eğer performans sıkıntı yaşarsanız haritalarda bana ulaşın.

NOT 3: GIT LFS ile dae pushlayamama sorunu çözülmüştür.