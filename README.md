
# Under Pressure AUV - Week 1

ROS 2 Humble ve Gazebo Fortress kullanılarak geliştirilmiş
birinci hafta simülasyon ve haberleşme projesidir.

## 1. Kullanılan Teknolojiler

- Ubuntu 22.04 LTS (WSL 2 üzerinde geliştirildi)
- ROS 2 Humble
- Gazebo Fortress
- Python 3
- SDF 1.8
- ros_gz_bridge

## 2. Projenin Amacı

Sabit nesneler ve bir RGB kamera içeren Gazebo dünyası
oluşturmak, kamera görüntüsünü ROS 2'ye aktarmak ve
Publisher-Subscriber haberleşmesini gerçekleştirmek.

## 3. Simülasyon Dünyası

Dünya adı: up_test_world
Dünya dosyası: worlds/test_world.sdf

| Nesne | Konum (x, y, z) | Geometri |
|---|---|---|
| Zemin | (0, 0, -0.05) | 10x10x0.1 m kutu |
| Mavi engel | (-1.8, 0, 0.5) | Kutu |
| Yeşil engel | (1.8, 0, 0.75) | Silindir |
| Sarı duvar | (0, 2, 0.5) | Kutu |
| Kırmızı hedef | (0, 0, 0.5) | Küre |
| Sabit kamera | (0, -4, 2.2) | RGB kamera |

Bütün nesneler sabittir. Zemin ve engeller için
visual ve collision geometrileri tanımlanmıştır.

Kamera özellikleri:
- Çözünürlük: 640x480
- Görüntü formatı: RGB8
- Yayın hızı: 10 Hz
- Topic: /camera/image_raw

## 4. ROS Düğümleri

### heartbeat_publisher
/up/heartbeat topic'ine saniyede bir, adayın adını
ve artan sıra numarasını içeren String mesajı yayınlar.

### heartbeat_subscriber
/up/heartbeat topic'ine abone olur ve gelen
mesajları terminale yazdırır.

### camera_monitor
/camera/image_raw topic'ine abone olur.

Her saniye:
- Görüntü genişliğini
- Görüntü yüksekliğini
- Encoding bilgisini
- Alınan toplam mesaj sayısını

terminale yazdırır.

## 5. Topic Bilgileri

| Topic | ROS Mesaj Tipi |
|---|---|
| /up/heartbeat | std_msgs/msg/String |
| /camera/image_raw | sensor_msgs/msg/Image |

Kamera görüntüsü Gazebo'dan ROS 2'ye
ros_gz_bridge üzerinden aktarılır.

## 6. Kurulum

Gerekli ortam:
- Ubuntu 22.04
- ROS 2 Humble Desktop
- Gazebo Fortress
- ros_gz_bridge
- rqt_image_view
- colcon

Resmi kurulum belgeleri:
https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html
https://gazebosim.org/docs/fortress/install_ubuntu/

ROS 2 ve Gazebo paket depoları ayarlandıktan sonra:

```bash
sudo apt update
sudo apt install -y ros-humble-desktop \
  ros-humble-ros-gz \
  ros-humble-rqt-image-view \
  ignition-fortress \
  python3-colcon-common-extensions
```

Depoyu kendi çalışma alanınıza klonlayın:

```bash
mkdir -p ~/up_week1_ws/src
cd ~/up_week1_ws/src
git clone git@github.com:menosgrande00/under-pressure-week1.git up_week1
```

REPO_URL yerine projenin Git bağlantısını yazın.

Paketi derleyin:

```bash
source /opt/ros/humble/setup.bash
cd ~/up_week1_ws
colcon build --symlink-install
source install/setup.bash
```

## 7. Çalıştırma

```bash
ros2 launch up_week1 week1.launch.py
```

Bu komut:
- Gazebo dünyasını
- Kamera ROS köprüsünü
- camera_monitor düğümünü
- heartbeat_publisher düğümünü
- heartbeat_subscriber düğümünü

birlikte başlatır.

Kamera görüntüsünü ayrı terminalde açmak için:

```bash
source /opt/ros/humble/setup.bash
ros2 run rqt_image_view rqt_image_view /camera/image_raw
```

WSL 2 ortamında OGRE 2 grafik hatası nedeniyle
Gazebo'nun OGRE 1 ile çalıştırılması gerekmiştir.
Launch dosyası bu ayarla hazırlanmıştır.

## 8. Test Komutları

```bash
ros2 node list
ros2 topic list
ros2 topic info /camera/image_raw
ros2 topic hz /camera/image_raw
ros2 topic hz /up/heartbeat
ros2 topic echo /up/heartbeat
```

Kamera köprüsü durdurulduğunda camera_monitor
mesaj sayısının artmaması; köprü yeniden başlatıldığında
sayacın artmaya devam etmesi test edilmiştir.

Kamera ROS topic'inde yaklaşık 10 Hz ölçülmüştür.

## 9. Harici Kaynaklar ve Yapay Zeka Kullanımı

ROS 2 ve Gazebo resmi dokümantasyonlarından yararlanılmıştır.
Kod geliştirme, açıklama ve hata giderme aşamalarında
ChatGPT desteği kullanılmıştır.
