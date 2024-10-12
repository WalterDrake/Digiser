from django.db import models
from authentication.models import CustomUser
from .model1 import Document
from django.utils.translation import gettext_lazy as _


class Options:

    _REGISTER_TYPE = (
        ('0', "Không có thông tin"),
        ('1', "Đăng ký đúng Hạn"),
        ('2', "Đăng ký Lại"),
        ('3', "Ghi vào sổ việc khai tử tại cơ quan có thẩm quyền ở nước ngoài"),
        ('4', "Đăng ký quá hạn")
    )
    _SEX_TYPE = (
        ('1', "Nam"),
        ('2', "Nữ"),
        ('3', "Chưa xác định được giới tính")
    )
    _RESIDENCE_TYPE = (
        ('0', "Không có thông tin"),
        ('1', "Thường trú"),
        ('2', "Tạm trú"),
    )

    _IDENTIFICATION_TYPE = (
        ('1', "CMND"),
        ('2', "Hộ chiếu"),
        ('3', "Thẻ thường trú"),
        ('4', "Thẻ căn cước công dân"),
        ('5', "Giấy chứng minh quân đội nhân dân"),
        ('6', "Giấy chứng minh sĩ quan quân đội"),
        ('7', "Giấy chứng minh công an nhân dân"),
        ('8', "Giấy tờ khác"),
        ('0', "Để trống"),
    )

    _DANTOC_LIST = (('Khác', 'Khác'), ('Kinh', 'Kinh'), ('Ba Na', 'Ba Na'), ('Ba Na (A-la Công)', 'Ba Na (A-la Công)'), ('Ba Na (Bơ-nâm)', 'Ba Na (Bơ-nâm)'), ('Ba Na (ConKđe)', 'Ba Na (ConKđe)'), ('Ba Na (Giơ-lar)', 'Ba Na (Giơ-lar)'), ('Ba Na (Giơ-lâng)', 'Ba Na (Giơ-lâng)'), ('Ba Na (Kpăng Công)', 'Ba Na (Kpăng Công)'), ('Ba Na (Krem)', 'Ba Na (Krem)'), ('Ba Na (Roh)', 'Ba Na (Roh)'), ('Ba Na (Rơ-ngao)', 'Ba Na (Rơ-ngao)'), ('Ba Na (Tơ-lô)', 'Ba Na (Tơ-lô)'), ('Ba Na (Y-lăng)', 'Ba Na (Y-lăng)'), ('Bố Y', 'Bố Y'), ('Bố Y (Chủng Chá)', 'Bố Y (Chủng Chá)'), ('Bố Y (Trọng Gia)', 'Bố Y (Trọng Gia)'), ('Bố Y (Tu Di)', 'Bố Y (Tu Di)'), ('Bố Y (Tu Din)', 'Bố Y (Tu Din)'), ('Brâu', 'Brâu'), ('Brâu (Brao)', 'Brâu (Brao)'), ('Bru Vân Kiều', 'Bru Vân Kiều'), ('Bru Vân Kiều (Bru)', 'Bru Vân Kiều (Bru)'), ('Bru Vân Kiều (Măng Coong)', 'Bru Vân Kiều (Măng Coong)'), ('Bru Vân Kiều (Tri Khùa)', 'Bru Vân Kiều (Tri Khùa)'), ('Bru Vân Kiều (Vân Kiều)', 'Bru Vân Kiều (Vân Kiều)'), ('Chăm', 'Chăm'), ('Chăm (Chàm)', 'Chăm (Chàm)'), ('Chăm (Chiêm Thành)', 'Chăm (Chiêm Thành)'), ('Chăm (Hroi)', 'Chăm (Hroi)'), ('Chơ Ro', 'Chơ Ro'), ('Chơ Ro (Châu-ro)', 'Chơ Ro (Châu-ro)'), ('Chơ Ro (Dơ-ro)', 'Chơ Ro (Dơ-ro)'), ('Chu Ru', 'Chu Ru'), ('Chu Ru (Chơ-ru)', 'Chu Ru (Chơ-ru)'), ('Chu Ru (Chu)', 'Chu Ru (Chu)'), ('Chứt', 'Chứt'), ('Chứt (A-rem)', 'Chứt (A-rem)'), ('Chứt (Chà-củi)', 'Chứt (Chà-củi)'), ('Chứt (Mã-liêng)', 'Chứt (Mã-liêng)'), ('Chứt (Máy)', 'Chứt (Máy)'), ('Chứt (Pa-leng)', 'Chứt (Pa-leng)'), ('Chứt (Rục)', 'Chứt (Rục)'), ('Chứt (Sách)', 'Chứt (Sách)'), ('Chứt (Tắc-củi)', 'Chứt (Tắc-củi)'), ('Chứt (Tơ-hung)', 'Chứt (Tơ-hung)'), ('Chứt (Tu vang)', 'Chứt (Tu vang)'), ('Chứt (U-mo)', 'Chứt (U-mo)'), ('Chứt (Xá Lá Vàng)', 'Chứt (Xá Lá Vàng)'), ('Chứt (Xơ-Lang)', 'Chứt (Xơ-Lang)'), ('Co', 'Co'), ('Co (Col)', 'Co (Col)'), ('Co (Cor)', 'Co (Cor)'), ('Co (Cùa)', 'Co (Cùa)'), ('Co (Trầu)', 'Co (Trầu)'), ('Cống', 'Cống'), ('Cống (Mấng Nhé)', 'Cống (Mấng Nhé)'), ('Cống (Xá Xeng)', 'Cống (Xá Xeng)'), ('Cống (Xắm Khống)', 'Cống (Xắm Khống)'), ('Cơ Ho', 'Cơ Ho'), ('Cơ Ho (Chil)', 'Cơ Ho (Chil)'), ('Cơ Ho (Cơ-don)', 'Cơ Ho (Cơ-don)'), ('Cơ Ho (Kơ Ho)', 'Cơ Ho (Kơ Ho)'), ('Cơ Ho (Lach)', 'Cơ Ho (Lach)'), ('Cơ Ho (Lat)', 'Cơ Ho (Lat)'), ('Cơ Ho (Nốp)', 'Cơ Ho (Nốp)'), ('Cơ Ho (Trinh)', 'Cơ Ho (Trinh)'), ('Cơ Ho (Tu-lốp)', 'Cơ Ho (Tu-lốp)'), ('Cơ Ho (Xrê)', 'Cơ Ho (Xrê)'), ('Cơ Lao', 'Cơ Lao'), ('Cơ Tu', 'Cơ Tu'), ('Cơ Tu (Cao)', 'Cơ Tu (Cao)'), ('Cơ Tu (Ca-tang)', 'Cơ Tu (Ca-tang)'), ('Cơ Tu (Ca-tu)', 'Cơ Tu (Ca-tu)'), ('Cơ Tu (Hạ)', 'Cơ Tu (Hạ)'), ('Cơ Tu (Phương)', 'Cơ Tu (Phương)'), ('Dao', 'Dao'), ('Dao (Cóc Mùn)', 'Dao (Cóc Mùn)'), ('Dao (Cóc Ngáng)', 'Dao (Cóc Ngáng)'), ('Dao (Dao Đỏ)', 'Dao (Dao Đỏ)'), ('Dao (Dao Tiền)', 'Dao (Dao Tiền)'), ('Dao (Dìu)', 'Dao (Dìu)'), ('Dao (Đại Bản)', 'Dao (Đại Bản)'), ('Dao (Động)', 'Dao (Động)'), ('Dao (Kiềm)', 'Dao (Kiềm)'), ('Dao (Lan Tẻn)', 'Dao (Lan Tẻn)'), ('Dao (Lô Giang)', 'Dao (Lô Giang)'), ('Dao (Mán)', 'Dao (Mán)'), ('Dao (Miên)', 'Dao (Miên)'), ('Dao (Miền)', 'Dao (Miền)'), ('Dao (Quần Chẹt)', 'Dao (Quần Chẹt)'), ('Dao (Quần Trắng)', 'Dao (Quần Trắng)'), ('Dao (Sơn Đầu)', 'Dao (Sơn Đầu)'), ('Dao (Thanh Y)', 'Dao (Thanh Y)'), ('Dao (Tiểu Bản)', 'Dao (Tiểu Bản)'), ('Dao (Trại)', 'Dao (Trại)'), ('Dao (Xá)', 'Dao (Xá)'), ('Ê Đê', 'Ê Đê'), ('Ê Đê (A-đham)', 'Ê Đê (A-đham)'), ('Ê Đê (Bih)', 'Ê Đê (Bih)'), ('Ê Đê (Blô)', 'Ê Đê (Blô)'), ('Ê Đê (Đê)', 'Ê Đê (Đê)'), ('Ê Đê (Đliê Ruê)', 'Ê Đê (Đliê Ruê)'), ('Ê Đê (Epan)', 'Ê Đê (Epan)'), ('Ê Đê (Kpạ)', 'Ê Đê (Kpạ)'), ('Ê Đê (Krung)', 'Ê Đê (Krung)'), ('Ê Đê (Ktul)', 'Ê Đê (Ktul)'), ('Ê Đê (Mđhur)', 'Ê Đê (Mđhur)'), ('Ê Đê (Ra-đê)', 'Ê Đê (Ra-đê)'), ('Gia Rai', 'Gia Rai'), ('Gia Rai (Chor)', 'Gia Rai (Chor)'), ('Gia Rai (Chơ-rai)', 'Gia Rai (Chơ-rai)'), ('Gia Rai (Giơ-rai)', 'Gia Rai (Giơ-rai)'), ('Gia Rai (Hđrung)', 'Gia Rai (Hđrung)'), ('Gia Rai (Hơ-bau)', 'Gia Rai (Hơ-bau)'), ('Gia Rai (Tơ-buăn)', 'Gia Rai (Tơ-buăn)'), ('Giáy', 'Giáy'), ('Giáy (Cùi Chu)', 'Giáy (Cùi Chu)'), ('Giáy (Dẩng)', 'Giáy (Dẩng)'), ('Giáy (Nhắng)', 'Giáy (Nhắng)'), ('Giáy (Pầu Thìn Nu Nà)', 'Giáy (Pầu Thìn Nu Nà)'), ('Giáy (Xa)', 'Giáy (Xa)'), ('Giẻ-Triêng', 'Giẻ-Triêng'), ('Giẻ-Triêng (Ca-tang)', 'Giẻ-Triêng (Ca-tang)'), ('Giẻ-Triêng (Đgiéh)', 'Giẻ-Triêng (Đgiéh)'), ('Giẻ-Triêng (Giang Rẫy Pin)', 'Giẻ-Triêng (Giang Rẫy Pin)'), ('Giẻ-Triêng (Gié Triêng)', 'Giẻ-Triêng (Gié Triêng)'), ('Giẻ-Triêng (La-ve)', 'Giẻ-Triêng (La-ve)'), ('Giẻ-Triêng (Tareb)', 'Giẻ-Triêng (Tareb)'), ('Giẻ-Triêng (Ta-riêng)', 'Giẻ-Triêng (Ta-riêng)'), ('Giẻ-Triêng (Treng)', 'Giẻ-Triêng (Treng)'), ('Giẻ-Triêng (Triêng)', 'Giẻ-Triêng (Triêng)'), ('Giẻ-Triêng (Ve)', 'Giẻ-Triêng (Ve)'), ('Giẻ-Triêng (Veh)', 'Giẻ-Triêng (Veh)'), ('Hà Nhì', 'Hà Nhì'), ('Hà Nhì (U Ni)', 'Hà Nhì (U Ni)'), ('Hà Nhì (Xá U Ni)', 'Hà Nhì (Xá U Ni)'), ('Hoa', 'Hoa'), ('Hoa (Hạ)', 'Hoa (Hạ)'), ('Hoa (Hải Nam)', 'Hoa (Hải Nam)'), ('Hoa (Hán)', 'Hoa (Hán)'), ('Hoa (Phúc Kiến)', 'Hoa (Phúc Kiến)'), ('Hoa (Quảng Đông)', 'Hoa (Quảng Đông)'), ('Hoa (Triều Châu)', 'Hoa (Triều Châu)'), ('Hoa (Xạ Phạng)', 'Hoa (Xạ Phạng)'), ('Hrê', 'Hrê'), ('Hrê (Chăm Rê)', 'Hrê (Chăm Rê)'), ('Hrê (Chom)', 'Hrê (Chom)'), ('Hrê (Krẹ Luỹ)', 'Hrê (Krẹ Luỹ)'), ('Kháng', 'Kháng'), ('Kháng (Quảng Lâm)', 'Kháng (Quảng Lâm)'), ('Kháng (Xá Ái)', 'Kháng (Xá Ái)'), ('Kháng (Xá Bung)', 'Kháng (Xá Bung)'), ('Kháng (Xá Dẩng)', 'Kháng (Xá Dẩng)'), ('Kháng (Xá Dón)', 'Kháng (Xá Dón)'), ('Kháng (Xá Hốc)', 'Kháng (Xá Hốc)'), ('Kháng (Xá Khao)', 'Kháng (Xá Khao)'), ('Kháng (Xá Súa)', 'Kháng (Xá Súa)'), ('Khơ Me', 'Khơ Me'), ('Khơ Me (Cu)', 'Khơ Me (Cu)'), ('Khơ Me (Cul)', 'Khơ Me (Cul)'), ('Khơ Me (Cur)', 'Khơ Me (Cur)'), ('Khơ Me (Khmer)', 'Khơ Me (Khmer)'), ('Khơ Me (Krôm)', 'Khơ Me (Krôm)'),
                    ('Khơ Me (Thổ)', 'Khơ Me (Thổ)'), ('Khơ Me (Việt gốc Miên)', 'Khơ Me (Việt gốc Miên)'), ('Khơ mú', 'Khơ mú'), ('Khơ mú (Mứn Xen)', 'Khơ mú (Mứn Xen)'), ('Khơ mú (Pu Thênh)', 'Khơ mú (Pu Thênh)'), ('Khơ mú (Tày Hay)', 'Khơ mú (Tày Hay)'), ('Khơ mú (Tềnh)', 'Khơ mú (Tềnh)'), ('Khơ mú (Xá Cẩu)', 'Khơ mú (Xá Cẩu)'), ('La Chí', 'La Chí'), ('La Chí (Cù Tê)', 'La Chí (Cù Tê)'), ('La Chí (La Quả)', 'La Chí (La Quả)'), ('La Ha', 'La Ha'), ('La Ha (Khlá Phlạo)', 'La Ha (Khlá Phlạo)'), ('La Ha (Xá Khao)', 'La Ha (Xá Khao)'), ('La Hủ', 'La Hủ'), ('La Hủ (Cò Xung)', 'La Hủ (Cò Xung)'), ('La Hủ (Khả Quy)', 'La Hủ (Khả Quy)'), ('La Hủ (Khù Xung)', 'La Hủ (Khù Xung)'), ('La Hủ (Lao)', 'La Hủ (Lao)'), ('La Hủ (Pu Đang)', 'La Hủ (Pu Đang)'), ('Lào', 'Lào'), ('Lào (Là Bốc)', 'Lào (Là Bốc)'), ('Lào (Lào Nọi)', 'Lào (Lào Nọi)'), ('Lô Lô', 'Lô Lô'), ('Lô Lô (Mun Di)', 'Lô Lô (Mun Di)'), ('Lự', 'Lự'), ('Lự (Duôn)', 'Lự (Duôn)'), ('Lự (Lừ)', 'Lự (Lừ)'), ('Lự (Nhuồn)', 'Lự (Nhuồn)'), ('Mạ', 'Mạ'), ('Mạ (Châu Mạ)', 'Mạ (Châu Mạ)'), ('Mạ (Mạ Krung)', 'Mạ (Mạ Krung)'), ('Mạ (Mạ Ngăn)', 'Mạ (Mạ Ngăn)'), ('Mạ (Mạ Tô)', 'Mạ (Mạ Tô)'), ('Mạ (Mạ Xóp)', 'Mạ (Mạ Xóp)'), ('Mảng', 'Mảng'), ('Mảng (Mảng Ư)', 'Mảng (Mảng Ư)'), ('Mảng (Xá Lá Vàng)', 'Mảng (Xá Lá Vàng)'), ('Mnông', 'Mnông'), ('Mnông (Biat)', 'Mnông (Biat)'), ('Mnông (Bu-đâng)', 'Mnông (Bu-đâng)'), ('Mnông (Chil)', 'Mnông (Chil)'), ('Mnông (ĐiPri)', 'Mnông (ĐiPri)'), ('Mnông (Gar)', 'Mnông (Gar)'), ('Mnông (Nông)', 'Mnông (Nông)'), ('Mnông (Pnông)', 'Mnông (Pnông)'), ('Mnông (Pré)', 'Mnông (Pré)'), ('Mnông (Rơ-lam)', 'Mnông (Rơ-lam)'), ('Mông', 'Mông'), ('Mông (HMông)', 'Mông (HMông)'), ('Mông (Hmông)', 'Mông (Hmông)'), ('Mông (Hoa)', 'Mông (Hoa)'), ('Mông (HơMông)', 'Mông (HơMông)'), ('Mông (Mán Trắng)', 'Mông (Mán Trắng)'), ('Mông (Mèo)', 'Mông (Mèo)'), ('Mông (Mèo Đen)', 'Mông (Mèo Đen)'), ('Mông (Mèo Đỏ)', 'Mông (Mèo Đỏ)'), ('Mông (Mèo Xanh)', 'Mông (Mèo Xanh)'), ('Mông (Ná Mẻo)', 'Mông (Ná Mẻo)'), ('Mường', 'Mường'), ('Mường (Ao Tá)', 'Mường (Ao Tá)'), ('Mường (Mọi)', 'Mường (Mọi)'), ('Mường (Mọi Bi)', 'Mường (Mọi Bi)'), ('Mường (Mol)', 'Mường (Mol)'), ('Mường (Mual)', 'Mường (Mual)'), ('Mường (Ậu Tá)', 'Mường (Ậu Tá)'), ('Ngái', 'Ngái'), ('Ngái (Đản)', 'Ngái (Đản)'), ('Ngái (Khách Gia)', 'Ngái (Khách Gia)'), ('Ngái (Lê)', 'Ngái (Lê)'), ('Ngái (Xín)', 'Ngái (Xín)'), ('Người nước ngoài', 'Người nước ngoài'), ('Nùng', 'Nùng'), ('Nùng (Giang)', 'Nùng (Giang)'), ('Nùng (Khèn Lài)', 'Nùng (Khèn Lài)'), ('Nùng (Nùng An)', 'Nùng (Nùng An)'), ('Nùng (Nùng Cháo)', 'Nùng (Nùng Cháo)'), ('Nùng (Nùng Lòi)', 'Nùng (Nùng Lòi)'), ('Nùng (Phàn Sinh)', 'Nùng (Phàn Sinh)'), ('Nùng (Quý Rim)', 'Nùng (Quý Rim)'), ('Nùng (Xuồng)', 'Nùng (Xuồng)'), ('Null', 'Null'), ('Ơ Đu', 'Ơ Đu'), ('Ơ Đu (Tày Hạt)', 'Ơ Đu (Tày Hạt)'), ('Pà Thẻn', 'Pà Thẻn'), ('Pà Thẻn (Pà Hưng)', 'Pà Thẻn (Pà Hưng)'), ('Pà Thẻn (Tống)', 'Pà Thẻn (Tống)'), ('Phù Lá', 'Phù Lá'), ('Phù Lá (Bồ Khô Pạ)', 'Phù Lá (Bồ Khô Pạ)'), ('Phù Lá (Mu Di Pạ Xá)', 'Phù Lá (Mu Di Pạ Xá)'), ('Phù Lá (Phó)', 'Phù Lá (Phó)'), ('Phù Lá (Phổ)', 'Phù Lá (Phổ)'), ('Phù Lá (Va Xơ)', 'Phù Lá (Va Xơ)'), ('Pu Péo', 'Pu Péo'), ('Pu Péo (Ka Pèo)', 'Pu Péo (Ka Pèo)'), ('Pu Péo (Pen Ti Lô Lô)', 'Pu Péo (Pen Ti Lô Lô)'), ('RaGlay', 'RaGlay'), ('RaGlay (La-oang)', 'RaGlay (La-oang)'), ('RaGlay (Noang)', 'RaGlay (Noang)'), ('RaGlay (Ra-clây)', 'RaGlay (Ra-clây)'), ('RaGlay (Ra-glai)', 'RaGlay (Ra-glai)'), ('RaGlay (Rai)', 'RaGlay (Rai)'), ('Rơ Măm', 'Rơ Măm'), ('Sán Chay', 'Sán Chay'), ('Sán Chay (Cao Lan)', 'Sán Chay (Cao Lan)'), ('Sán Chay (Hờn Bạn)', 'Sán Chay (Hờn Bạn)'), ('Sán Chay (Mán Cao Lan)', 'Sán Chay (Mán Cao Lan)'), ('Sán Chay (Sán Chỉ)', 'Sán Chay (Sán Chỉ)'), ('Sán Chay (Sơn Tử)', 'Sán Chay (Sơn Tử)'), ('Sán Dìu', 'Sán Dìu'), ('Sán Dìu (Mán)', 'Sán Dìu (Mán)'), ('Sán Dìu (Quần Cộc)', 'Sán Dìu (Quần Cộc)'), ('Sán Dìu (Sán Dẻo)', 'Sán Dìu (Sán Dẻo)'), ('Sán Dìu (Trại)', 'Sán Dìu (Trại)'), ('Sán Dìu (Trại Đất)', 'Sán Dìu (Trại Đất)'), ('Si La', 'Si La'), ('Si La (Cù Dề Xừ)', 'Si La (Cù Dề Xừ)'), ('Si La (Khả pẻ)', 'Si La (Khả pẻ)'), ('Tà Ôi', 'Tà Ôi'), ('Tà Ôi (Ba-hi)', 'Tà Ôi (Ba-hi)'), ('Tà Ôi (Pa-co)', 'Tà Ôi (Pa-co)'), ('Tà Ôi (Pa-hi)', 'Tà Ôi (Pa-hi)'), ('Tà Ôi (Tôi-ôi)', 'Tà Ôi (Tôi-ôi)'), ('Tày', 'Tày'), ('Tày (Ngạn)', 'Tày (Ngạn)'), ('Tày (Pa Dí)', 'Tày (Pa Dí)'), ('Tày (Phén)', 'Tày (Phén)'), ('Tày (Tày Khao)', 'Tày (Tày Khao)'), ('Tày (Thổ)', 'Tày (Thổ)'), ('Tày (Thù Lao)', 'Tày (Thù Lao)'), ('Thái', 'Thái'), ('Thái (Hàng Bông)', 'Thái (Hàng Bông)'), ('Thái (Mán Thanh)', 'Thái (Mán Thanh)'), ('Thái (Pa Thay)', 'Thái (Pa Thay)'), ('Thái (Tày Đăm)', 'Thái (Tày Đăm)'), ('Thái (Tày Mười)', 'Thái (Tày Mười)'), ('Thái (Tày Mường)', 'Thái (Tày Mường)'), ('Thái (Tày Thanh)', 'Thái (Tày Thanh)'), ('Thái (Thổ Đà Bắc)', 'Thái (Thổ Đà Bắc)'), ('Thổ', 'Thổ'), ('Thổ (Con Kha)', 'Thổ (Con Kha)'), ('Thổ (Cuối)', 'Thổ (Cuối)'), ('Thổ (Đan Lai)', 'Thổ (Đan Lai)'), ('Thổ (Họ)', 'Thổ (Họ)'), ('Thổ (Kẹo)', 'Thổ (Kẹo)'), ('Thổ (Ly Hà)', 'Thổ (Ly Hà)'), ('Thổ (Mọn)', 'Thổ (Mọn)'), ('Thổ (Tày Pọng)', 'Thổ (Tày Pọng)'), ('Thổ (Xá Lá Vàng)', 'Thổ (Xá Lá Vàng)'), ('Xinh Mun', 'Xinh Mun'), ('Xinh Mun (Pụa)', 'Xinh Mun (Pụa)'), ('Xinh Mun (Puộc)', 'Xinh Mun (Puộc)'), ('Xơ Đăng', 'Xơ Đăng'), ('Xơ Đăng (Bri-la)', 'Xơ Đăng (Bri-la)'), ('Xơ Đăng (Ca-dong)', 'Xơ Đăng (Ca-dong)'), ('Xơ Đăng (ConLan)', 'Xơ Đăng (ConLan)'), ('Xơ Đăng (Ha-lăng)', 'Xơ Đăng (Ha-lăng)'), ('Xơ Đăng (Hđang)', 'Xơ Đăng (Hđang)'), ('Xơ Đăng (Kmrâng)', 'Xơ Đăng (Kmrâng)'), ('Xơ Đăng (Mơ-nâm)', 'Xơ Đăng (Mơ-nâm)'), ('Xơ Đăng (Tang)', 'Xơ Đăng (Tang)'), ('Xơ Đăng (Tơ-đra)', 'Xơ Đăng (Tơ-đra)'), ('Xơ Đăng (Xơ-teng)', 'Xơ Đăng (Xơ-teng)'), ('Xtiêng', 'Xtiêng'), ('Xtiêng (Xa-điêng)', 'Xtiêng (Xa-điêng)'))
    _COUNTRIES_LIST = (('Không có thông tin', 'Không có thông tin'), ('Việt Nam', 'Việt Nam'), ('Ác-hen-ti-na (Argentine / Argentinian)', 'Ác-hen-ti-na (Argentine / Argentinian)'), ('Ác-mê-ni-a (Albanian)', 'Ác-mê-ni-a (Albanian)'), ('A-déc-bai-gian (Azerbaijani)', 'A-déc-bai-gian (Azerbaijani)'), ('Ai Cập (Egyptian)', 'Ai Cập (Egyptian)'), ('Ai len (Irish)', 'Ai len (Irish)'), ('Ai-xơ-len (Icelandic)', 'Ai-xơ-len (Icelandic)'), ('Aland Islands', 'Aland Islands'), ('American Samoa', 'American Samoa'), ('An-ba-ni (Albanian)', 'An-ba-ni (Albanian)'), ('An-đô-ra (Andorran)', 'An-đô-ra (Andorran)'), ('An-giê-ri (Algerian)', 'An-giê-ri (Algerian)'), ('Anh (British)', 'Anh (British)'), ('Áo (Austrian)', 'Áo (Austrian)'), ('Áp-ganitxtan', 'Áp-ganitxtan'), ('A-rập thống nhất (Emirian)', 'A-rập thống nhất (Emirian)'), ('A-rập Xa-ra-uy (Western Sahara)', 'A-rập Xa-ra-uy (Western Sahara)'), ('A-rập Xê-út (Saudi Arabian)', 'A-rập Xê-út (Saudi Arabian)'), ('A-ru-ba (Aruba)', 'A-ru-ba (Aruba)'), ('Ăng-gô-la (Angolan)', 'Ăng-gô-la (Angolan)'), ('Ăng-gui-la (Anguilla)', 'Ăng-gui-la (Anguilla)'), ('Ăng-ti-gua và Bác-bu-đa (Antigua and Barbuda)', 'Ăng-ti-gua và Bác-bu-đa (Antigua and Barbuda)'), ('Ba Lan (Polish)', 'Ba Lan (Polish)'), ('Bác-ba-đốt (Barbadian)', 'Bác-ba-đốt (Barbadian)'), ('Ba-ha-ma (Bahamas)', 'Ba-ha-ma (Bahamas)'), ('Ba-ranh (Bahraini)', 'Ba-ranh (Bahraini)'), ('Băng-la-đét (Bangladeshi)', 'Băng-la-đét (Bangladeshi)'), ('Béc-mu-đa (Bermuda)', 'Béc-mu-đa (Bermuda)'), ('Bê-la-rút (Belarusian)', 'Bê-la-rút (Belarusian)'), ('Bê-li-xê (Belizean)', 'Bê-li-xê (Belizean)'), ('Bê-nanh (Beninese)', 'Bê-nanh (Beninese)'), ('Bỉ (Belgian)', 'Bỉ (Belgian)'), ('Bồ Đào Nha (Portuguese)', 'Bồ Đào Nha (Portuguese)'), ('Bô-li-vi-a (Bolivian)', 'Bô-li-vi-a (Bolivian)'), ('Bốt-xoa-na (Botswanan)', 'Bốt-xoa-na (Botswanan)'), ('Bô-xni-a Héc-dê-gô-vi-na (Bosnian, Herzegovinian)', 'Bô-xni-a Héc-dê-gô-vi-na (Bosnian, Herzegovinian)'), ('Bra-xin (Brazilian)', 'Bra-xin (Brazilian)'), ('British Indian Ocean Territory', 'British Indian Ocean Territory'), ('British Virgin Islands', 'British Virgin Islands'), ('Bru-nây (Bruneian)', 'Bru-nây (Bruneian)'), ('Bun-ga-ri (Bulgarian)', 'Bun-ga-ri (Bulgarian)'), ('Buốc-ki-na Pha-xô (Burkinabe)', 'Buốc-ki-na Pha-xô (Burkinabe)'), ('Bu-run-đi (Burundian)', 'Bu-run-đi (Burundian)'), ('Bu-tan (Bhutan)', 'Bu-tan (Bhutan)'), ('Ca-mơ-run (Cameroonian)', 'Ca-mơ-run (Cameroonian)'), ('Ca-na-đa (Canadian)', 'Ca-na-đa (Canadian)'), ('Cáp-ve (Cape Verdian)', 'Cáp-ve (Cape Verdian)'), ('Ca-ta (Qatari)', 'Ca-ta (Qatari)'), ('Căm-pu-chia (Cambodian)', 'Căm-pu-chia (Cambodian)'), ('CH Tơ-ri-ni-đát và Tô-ba-gô (Trinidad and Tobago)', 'CH Tơ-ri-ni-đát và Tô-ba-gô (Trinidad and Tobago)'), ('Chi-lê (Chilean)', 'Chi-lê (Chilean)'), ('Cô-lôm-bi-a (Colombian)', 'Cô-lôm-bi-a (Colombian)'), ('Cô-mo (Comoros)', 'Cô-mo (Comoros)'), ('Cộng hòa dân chủ Công-gô', 'Cộng hòa dân chủ Công-gô'), ('Công-gô (Congolese)', 'Công-gô (Congolese)'), ('Cô-oét (Kuwaiti)', 'Cô-oét (Kuwaiti)'), ('Cốt-đi-voa (Ivorian)', 'Cốt-đi-voa (Ivorian)'), ('Cô-xta Ri-ca (Costa Rica)', 'Cô-xta Ri-ca (Costa Rica)'), ('Crô-a-ti-a (Croatian)', 'Crô-a-ti-a (Croatian)'), ('Cu-ba (Cuban)', 'Cu-ba (Cuban)'), ('Cư-rơ-gư-dơ-xtan (Kyrgyzstan)', 'Cư-rơ-gư-dơ-xtan (Kyrgyzstan)'), ('Dăm-bi-a (Zambian)', 'Dăm-bi-a (Zambian)'), ('Dim-ba-bu-ê (Zimbabwean)', 'Dim-ba-bu-ê (Zimbabwean)'), ('Đan Mạch (Danis)', 'Đan Mạch (Danis)'), ('Đảo Bô-u-vet (Bouvet Island)', 'Đảo Bô-u-vet (Bouvet Island)'), ('Đảo Chri-xma (Christmas Island)', 'Đảo Chri-xma (Christmas Island)'), ('Đảo Nô-fốc (Norfolk Island)', 'Đảo Nô-fốc (Norfolk Island)'), ('Đảo Xanh Hê-lê-na (Saint Helena)', 'Đảo Xanh Hê-lê-na (Saint Helena)'), ('Đô-mi-ni-ca (Dominicain)', 'Đô-mi-ni-ca (Dominicain)'), ('Đô-mi-ni-ca-na (Dominican)', 'Đô-mi-ni-ca-na (Dominican)'), ('Đông Ti-mo (East Timorese)', 'Đông Ti-mo (East Timorese)'), ('Đức (German)', 'Đức (German)'), ('En Xan-va-đo (EL Salvadorian)', 'En Xan-va-đo (EL Salvadorian)'), ('Ê-cu-a-đo (Ecuadorian)', 'Ê-cu-a-đo (Ecuadorian)'), ('Ê-ri-tơ-ri-a (Eritrean)', 'Ê-ri-tơ-ri-a (Eritrean)'), ('Ê-ti-ô-pi-a (Ethiopian)', 'Ê-ti-ô-pi-a (Ethiopian)'), ('Ê-xtô-ni-a (Estonian)', 'Ê-xtô-ni-a (Estonian)'), ('Ga-bông (Gabonese)', 'Ga-bông (Gabonese)'), ('Găm-bi-a ( Gambian)', 'Găm-bi-a ( Gambian)'), ('Gha-na (Ghanaian)', 'Gha-na (Ghanaian)'), ('Ghi-nê Bít-xao (Guinea-Bissauan)', 'Ghi-nê Bít-xao (Guinea-Bissauan)'), ('Ghi-nê (Guinean)', 'Ghi-nê (Guinean)'), ('Ghi-nê Xích đạo (Equatorial Guinean)', 'Ghi-nê Xích đạo (Equatorial Guinean)'), ('Gi-bran-ta (Gibraltar)', 'Gi-bran-ta (Gibraltar)'), ('Gi-bu-ti (Djiboutian)', 'Gi-bu-ti (Djiboutian)'), ('Giê-óoc-gi-a (Gruzian)', 'Giê-óoc-gi-a (Gruzian)'), ('Gioóc-đa-ni (Jordanian)', 'Gioóc-đa-ni (Jordanian)'), ('Goa-tê-ma-la (Guatemalan)', 'Goa-tê-ma-la (Guatemalan)'), ('Grê-na-đa (Grenadian)', 'Grê-na-đa (Grenadian)'), ('Grin-lơn (Greenland)', 'Grin-lơn (Greenland)'), ('Gua-đờ-lúp (Guadeloupe)', 'Gua-đờ-lúp (Guadeloupe)'), ('Gu-am (Guam)', 'Gu-am (Guam)'), ('Guernsey', 'Guernsey'), ('Guy-a-na (Guyanese)', 'Guy-a-na (Guyanese)'), ('Guy-a-na thuộc Pháp (French Guiana)', 'Guy-a-na thuộc Pháp (French Guiana)'), ('Hà Lan (Dutch)', 'Hà Lan (Dutch)'), ('Ha-i-ti (Haitian)', 'Ha-i-ti (Haitian)'), ('Hàn Quốc (South Korean)', 'Hàn Quốc (South Korean)'), ('Hoa Kỳ (American)', 'Hoa Kỳ (American)'), ('Hung-ga-ry (Hungarian)', 'Hung-ga-ry (Hungarian)'), ('Hy Lạp (Greek)', 'Hy Lạp (Greek)'), ('In-đô-nê-xi-a (Indonesian)', 'In-đô-nê-xi-a (Indonesian)'), ('I-ran (Iranian)', 'I-ran (Iranian)'), ('I-rắc (Iraqi)', 'I-rắc (Iraqi)'), ('Isle of Man', 'Isle of Man'), ('I-ta-li-a (Italian)', 'I-ta-li-a (Italian)'), ('Ix-ra-en (Israeli)', 'Ix-ra-en (Israeli)'), ('Ja-mai-ca (Jamaican)', 'Ja-mai-ca (Jamaican)'), ('Jersey', 'Jersey'), ('Ka-dắc-xtan (Kazakh / Kazakhstani)', 'Ka-dắc-xtan (Kazakh / Kazakhstani)'), ('Kê-ni-a (Kenyan)', 'Kê-ni-a (Kenyan)'), ('Ki-ri-ba-ti (Kiribati)', 'Ki-ri-ba-ti (Kiribati)'), ('Lào (Laotian)', 'Lào (Laotian)'), ('Lát-vi-a (Latvian)', 'Lát-vi-a (Latvian)'), ('Lê-xô-thô (Lesotho)', 'Lê-xô-thô (Lesotho)'), ('Li-băng (Lebanese)', 'Li-băng (Lebanese)'), ('Li-bê-ri-a (Liberia)', 'Li-bê-ri-a (Liberia)'), ('Li-bi (Libyan)', 'Li-bi (Libyan)'), ('Liên bang Xanh Kít và Nê-vít (Saint Kitts and Nevis)', 'Liên bang Xanh Kít và Nê-vít (Saint Kitts and Nevis)'), ('Lít-ten-xơ-tên (Liechtenstein)', 'Lít-ten-xơ-tên (Liechtenstein)'), ('Lít-va (Lithuanian)', 'Lít-va (Lithuanian)'), ('Lúc-xăm-bua (Luxembourg)', 'Lúc-xăm-bua (Luxembourg)'), ('Mac-ti-nic (Martinique)', 'Mac-ti-nic (Martinique)'), ('Ma-đa-gát-xca (Malagasy)', 'Ma-đa-gát-xca (Malagasy)'), ('Ma-lai-xi-a (Malaysian)', 'Ma-lai-xi-a (Malaysian)'), ('Ma-la-uy (Malawi)', 'Ma-la-uy (Malawi)'), ('Ma-li (Malian)', 'Ma-li (Malian)'), ('Man-đi-vơ (Maldivan)', 'Man-đi-vơ (Maldivan)'), ('Man-ta (Maltese)', 'Man-ta (Maltese)'), ('Ma-rốc (Moroccan)', 'Ma-rốc (Moroccan)'), ('Ma-xê-đô-ni-a (Macedonian)', 'Ma-xê-đô-ni-a (Macedonian)'), ('May-ôt (Mayotte)', 'May-ôt (Mayotte)'), ('Mê-hi-cô (Mexican)', 'Mê-hi-cô (Mexican)'),
                       ('Mi-an-ma (Burmese)', 'Mi-an-ma (Burmese)'), ('Mi-crô-nê-si-a (Micronesian)', 'Mi-crô-nê-si-a (Micronesian)'), ('Mô-dăm-bích (Mozambican)', 'Mô-dăm-bích (Mozambican)'), ('Mô-na-cô (Monaco)', 'Mô-na-cô (Monaco)'), ('Môn-đô-va (Moldovan)', 'Môn-đô-va (Moldovan)'), ('Mông Cổ (Mongolian)', 'Mông Cổ (Mongolian)'), ('Môn-tê-nê-grô (Montenegrin)', 'Môn-tê-nê-grô (Montenegrin)'), ('Môn-xê-rat (Montserrat)', 'Môn-xê-rat (Montserrat)'), ('Mô-ri-ta-ni (Mauritanian)', 'Mô-ri-ta-ni (Mauritanian)'), ('Mô-ri-xơ (Mauritian)', 'Mô-ri-xơ (Mauritian)'), ('Ấn Độ (Indian)', 'Ấn Độ (Indian)'), ('Na Uy (Norwegian)', 'Na Uy (Norwegian)'), ('Nam Cực (Antarctica)', 'Nam Cực (Antarctica)'), ('Nam Phi (South African)', 'Nam Phi (South African)'), ('Nam Su-dan (South Sudan)', 'Nam Su-dan (South Sudan)'), ('Nam-mi-bi-a (Namibian)', 'Nam-mi-bi-a (Namibian)'), ('Na-u-ru (Nauruan)', 'Na-u-ru (Nauruan)'), ('Nê-pan (Nepalese)', 'Nê-pan (Nepalese)'), ('Nga (Russian)', 'Nga (Russian)'), ('Người không quốc tịch (Stateless person)', 'Người không quốc tịch (Stateless person)'), ('Nhật Bản (Japanese)', 'Nhật Bản (Japanese)'), ('Ni-ca-ra-goa (Nicaraguan)', 'Ni-ca-ra-goa (Nicaraguan)'), ('Ni-giê (Nigerian)', 'Ni-giê (Nigerian)'), ('Ni-giê-ri-a (Nigierian)', 'Ni-giê-ri-a (Nigierian)'), ('Niu Ca-le-đô-ni-a (New Caledonia)', 'Niu Ca-le-đô-ni-a (New Caledonia)'), ('Niu di-lân (New Zealand)', 'Niu di-lân (New Zealand)'), ('Ni-u-ê (Niue)', 'Ni-u-ê (Niue)'), ('Ô-man (Omani)', 'Ô-man (Omani)'), ('Ôn-đu-rát (Honduran)', 'Ôn-đu-rát (Honduran)'), ('Ô-xtrây-li-a (Australian)', 'Ô-xtrây-li-a (Australian)'), ('Pa-ki-xtan (Pakistani)', 'Pa-ki-xtan (Pakistani)'), ('Pa-lau (Palauan)', 'Pa-lau (Palauan)'), ('Pa-le-xtin (palestinian)', 'Pa-le-xtin (palestinian)'), ('Pa-na-ma (Panamanian)', 'Pa-na-ma (Panamanian)'), ('Pa-pu-a Niu Ghi-nê (Papua New Guinean)', 'Pa-pu-a Niu Ghi-nê (Papua New Guinean)'), ('Pa-ra-goay (Paraguayan)', 'Pa-ra-goay (Paraguayan)'), ('Pê-ru (Peruvian)', 'Pê-ru (Peruvian)'), ('Pháp (French)', 'Pháp (French)'), ('Phần Lan (Finnish)', 'Phần Lan (Finnish)'), ('Phi-gi (Fijian)', 'Phi-gi (Fijian)'), ('Phi-líp-pin (Filipino)', 'Phi-líp-pin (Filipino)'), ('Pit-ca-in (Pitcairn)', 'Pit-ca-in (Pitcairn)'), ('Pô-li-nê-si-a thuộc Pháp (French Polynesia)', 'Pô-li-nê-si-a thuộc Pháp (French Polynesia)'), ('Pu-éc-tô-Ri-cô (Puerto Rico)', 'Pu-éc-tô-Ri-cô (Puerto Rico)'), ('Quần đảo An-ti thuộc Hà Lan (Netherlands Antilles)', 'Quần đảo An-ti thuộc Hà Lan (Netherlands Antilles)'), ('Quần đảo Cây-man (Cayman Islands)', 'Quần đảo Cây-man (Cayman Islands)'), ('Quần đảo Cúc (Cook Islands)', 'Quần đảo Cúc (Cook Islands)'), ('Quần đảo cừu', 'Quần đảo cừu'), ('Quần đảo dừa (Cocos Islands)', 'Quần đảo dừa (Cocos Islands)'), ('Quần đảo Hớt và Mac-đô-nan (Heard Island and Mcdonald Islands)', 'Quần đảo Hớt và Mac-đô-nan (Heard Island and Mcdonald Islands)'), ('Quần đảo Mác-san (Marshallese Islands)', 'Quần đảo Mác-san (Marshallese Islands)'), ('Quần đảo Man-vi-na (Malvinas)', 'Quần đảo Man-vi-na (Malvinas)'), ('Quần đảo Ma-ri-a-na (Northern Mariana Islands)', 'Quần đảo Ma-ri-a-na (Northern Mariana Islands)'), ('Quần đảo nhỏ thuộc Mỹ (United States Minor Outlying Islands)', 'Quần đảo nhỏ thuộc Mỹ (United States Minor Outlying Islands)'), ('Quần đảo Oa-li và Fu-tu-na (Wallis and Futuna Islands)', 'Quần đảo Oa-li và Fu-tu-na (Wallis and Futuna Islands)'), ('Quần đảo Tuc Và Ca-i-cô (Turks and Caicos Islands)', 'Quần đảo Tuc Và Ca-i-cô (Turks and Caicos Islands)'), ('Quần đảo Vi-gin (Mỹ)', 'Quần đảo Vi-gin (Mỹ)'), ('Quần đảo Xvan-ba và Gan Mai-en (Svalbard and Jan Mayen Islands)', 'Quần đảo Xvan-ba và Gan Mai-en (Svalbard and Jan Mayen Islands)'), ('Rê-u-ni-on (Réunion)', 'Rê-u-ni-on (Réunion)'), ('Ru-an-đa (Rwandan)', 'Ru-an-đa (Rwandan)'), ('Ru-ma-ni (Romanian)', 'Ru-ma-ni (Romanian)'), ('Saint-Barthélemy', 'Saint-Barthélemy'), ('Saint-Martin (French part)', 'Saint-Martin (French part)'), ('San Ma-ri-nô (San marino)', 'San Ma-ri-nô (San marino)'), ('Sao Tô-mê và Prin-xi-pê (Sao Tomean)', 'Sao Tô-mê và Prin-xi-pê (Sao Tomean)'), ('Sát (Chadian)', 'Sát (Chadian)'), ('Séc (Czech)', 'Séc (Czech)'), ('Si-ê-ra Lê-ôn (Sierra Leonean)', 'Si-ê-ra Lê-ôn (Sierra Leonean)'), ('Síp (Cypriot)', 'Síp (Cypriot)'), ('South Georgia and the South Sandwich Islands', 'South Georgia and the South Sandwich Islands'), ('Tan-da-ni-a (Tanzanian)', 'Tan-da-ni-a (Tanzanian)'), ('Tát-gi-ki-xtan (Tajik)', 'Tát-gi-ki-xtan (Tajik)'), ('Tây Ban Nha (Spanish)', 'Tây Ban Nha (Spanish)'), ('Thái Lan (Thai)', 'Thái Lan (Thai)'), ('Thổ Nhĩ Kỳ (Turkish)', 'Thổ Nhĩ Kỳ (Turkish)'), ('Thụy Điển (Swedish)', 'Thụy Điển (Swedish)'), ('Thụy Sĩ (Swiss)', 'Thụy Sĩ (Swiss)'), ('Tô-gô (Togolese)', 'Tô-gô (Togolese)'), ('Tô-ke-lau (Tokelau)', 'Tô-ke-lau (Tokelau)'), ('Tôn-ga (Tonga)', 'Tôn-ga (Tonga)'), ('Triều Tiên (North Korean)', 'Triều Tiên (North Korean)'), ('Trung Phi (Middle African)', 'Trung Phi (Middle African)'), ('Trung Quốc', 'Trung Quốc'), ('Trung Quốc (Đài Loan)', 'Trung Quốc (Đài Loan)'), ('Trung Quốc (Đài Loan) (Taiwanese)', 'Trung Quốc (Đài Loan) (Taiwanese)'), ('Trung Quốc (Hồng Công) (Hong Kong, Chinese)', 'Trung Quốc (Hồng Công) (Hong Kong, Chinese)'), ('Trung Quốc (Ma-cao) (Macau, Chinese)', 'Trung Quốc (Ma-cao) (Macau, Chinese)'), ('Tuốc-mê-ni-xtan (Turkmen(s))', 'Tuốc-mê-ni-xtan (Turkmen(s))'), ('Tu-va-lu (Tuvalu)', 'Tu-va-lu (Tuvalu)'), ('Tuy-ni-di (Tunisian)', 'Tuy-ni-di (Tunisian)'), ('U-crai-na (Ukrainian)', 'U-crai-na (Ukrainian)'), ('U-dơ-bê-ki-xtan (Uzbekistani)', 'U-dơ-bê-ki-xtan (Uzbekistani)'), ('U-gan-đa (Ugandan)', 'U-gan-đa (Ugandan)'), ('U-ru-goay (Uruguayan)', 'U-ru-goay (Uruguayan)'), ('Va-nu-a-tu (Ni-Vanuatu)', 'Va-nu-a-tu (Ni-Vanuatu)'), ('Va-ti-căng (Vatican )', 'Va-ti-căng (Vatican )'), ('Vê-nê-du-ê-la (Venezuelan)', 'Vê-nê-du-ê-la (Venezuelan)'), ('Vùng Nam Bán Cầu thuộc Pháp (French Southern Territories)', 'Vùng Nam Bán Cầu thuộc Pháp (French Southern Territories)'), ('Xa-moa (Samoan)', 'Xa-moa (Samoan)'), ('Xanh Lu-xi-a (Saint Lucia)', 'Xanh Lu-xi-a (Saint Lucia)'), ('Xanh Pi-ê và Mi-cơ-lông (Saint Pierre and Miquelon)', 'Xanh Pi-ê và Mi-cơ-lông (Saint Pierre and Miquelon)'), ('Xanh Vin-xen và Grê-na-đin (Saint Vincent and the Grenadines)', 'Xanh Vin-xen và Grê-na-đin (Saint Vincent and the Grenadines)'), ('Xây-sen (Seychellois)', 'Xây-sen (Seychellois)'), ('Xéc-bi-a (Serbian)', 'Xéc-bi-a (Serbian)'), ('Xê-nê-gan (Senegalese)', 'Xê-nê-gan (Senegalese)'), ('Xinh-ga-po (Singaporean)', 'Xinh-ga-po (Singaporean)'), ('Xlô-va-ki-a (Slovak / Slovakian)', 'Xlô-va-ki-a (Slovak / Slovakian)'), ('Xlô-ven-ni-a (Slovenian / Slovene)', 'Xlô-ven-ni-a (Slovenian / Slovene)'), ('Xoa-di-len (Swaziland)', 'Xoa-di-len (Swaziland)'), ('Xô-lô-môn (Solomon Islander)', 'Xô-lô-môn (Solomon Islander)'), ('Xô-ma-li (Somali)', 'Xô-ma-li (Somali)'), ('Xri Lan-ca (Sri Lankan)', 'Xri Lan-ca (Sri Lankan)'), ('Xu-đăng (Sudanese)', 'Xu-đăng (Sudanese)'), ('Xu-ri-nam (Surinamese)', 'Xu-ri-nam (Surinamese)'), ('Xy-ri (Syrian)', 'Xy-ri (Syrian)'), ('Y-ê-men (Yemeni / Yemenite)', 'Y-ê-men (Yemeni / Yemenite)'))

    _DEATH_CERT_TYPE = (
        ("0", "Không có thông tin"),
        ("1", "Giấy báo tử"),
        ("2", "Giấy xác nhận việc thi hành án tử hình"),
        ("3", "Bản án, quyết định có hiệu lực của Tòa án về việc tuyên bố một người là đã chết"),
        ("4", "Văn bản xác nhận của cơ quan công an hoặc kết quả giảm định của Cơ quan giám định pháp y"),
        ("5", "Văn bản xác định nguyên nhân chết của cơ quan y tế cấp huyện"),
        ("6", "Biên bản xác nhận việc chết"),
        ("7", "Văn bản xác nhận việc chết của người làm chứng"),
    )

    # Birth Certificate Document
    _BIRTH_CERT_TYPE = (
        ("1", "Đã xác định được cả cha lẫn mẹ"),
        ("2", "Chưa xác định được mẹ"),
        ("3", "Chưa xác định được cha"),
        ("4", "Chưa xác định được cả cha lẫn mẹ"),
        ("5", "Trẻ bị bỏ rơi"),
    )

    # Marriage Certificate
    _REGISTER_STATUS = (
        ("1", "Đăng ký lần đầu"),
        ("2", "Đăng ký lại"),
    )


    _MARRIED_STATUS = (
        ("Đã ly hôn", "Đã ly hôn"),
        ("Đã hủy việc kết hôn", "Đã hủy việc kết hôn"),
        ("Đã được công nhận việc kết hôn", "Đã được công nhận việc kết hôn"),
        ("Không có thông tin", "Không có thông tin"),
    )

    _INTENDED_USE = (
        ('1', "Để đăng ký kết hôn trong nước (với người Việt Nam)"),
        ('2', "Để đăng ký kết hôn trong nước (với người nước ngoài)"),
        ('3', "Để đăng ký kết hôn ở nước ngoài (với người Việt Nam)"),
        ('4', "Để đăng ký kết hôn ở nước ngoài (với người nước ngoài)"),
        ('5', "Mục đích khác"),
    )

    _CERTIFICATE_TYPE = (
        ("1", "Cha nhận con"),
        ("2", "Mẹ nhận con"),
        ("3", "Con nhận cha"),
        ("4", "Con nhận mẹ"),
    )

    _REGISTER_TYPE_PAC = (
        ("0", "Không có thông tin"),
        ("1", "Đăng ký mới"),
        ("2", "Ghi vào sổ việc nhận cha, mẹ, con đã được đăng ký tại cơ quan có thẩm quyền ở nước ngoài"),
    )


class Birth_Certificate_Document(models.Model):

    document = models.ForeignKey(
        Document, blank=True, null=True, on_delete=models.CASCADE)

    executor = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.SET_NULL)
    # Các trường thông tin cơ bản (10 trường)
    so = models.CharField(max_length=10,  null=True,
                          verbose_name='Số', blank=True)
    quyenSo = models.CharField(
        max_length=10,  null=True, verbose_name='Quyển Số', blank=True)
    trangSo = models.CharField(
        max_length=10,  null=True, verbose_name='Trang Số', blank=True)
    ngayDangKy = models.DateField(
        verbose_name='Ngày Đăng Ký', blank=True)
    loaiDangKy = models.CharField(max_length=1, choices=Options._REGISTER_TYPE,
                                  default='1', verbose_name='Loại Đăng Ký', blank=True)
    noiDangKy = models.CharField(
        max_length=100,  null=True, verbose_name='Nơi Đăng Ký', blank=True)
    nguoiKy = models.CharField(
        max_length=20,  null=True, verbose_name='Người Ký', blank=True)
    chucVuNguoiKy = models.CharField(
        max_length=30,  null=True, verbose_name="Chức Vụ Người Ký", blank=True)
    nguoiThucHien = models.CharField(
        max_length=50,  null=True, verbose_name="Người Thực Hiện", blank=True)
    ghiChu = models.CharField(
        max_length=100,  null=True, verbose_name="Ghi Chú", blank=True)

    # Thông tin về người được đăng ký khai sinh (11 trường)
    nksHoTen = models.CharField(
        max_length=30,  null=True, verbose_name='Họ Tên (Người Khai Sinh)', blank=True)
    nksGioiTinh = models.CharField(max_length=1, choices=Options._SEX_TYPE, verbose_name='Giới Tính (Người Khai Sinh)',
                                   default='3', blank=True)
    nksNgaySinh = models.DateField(
        verbose_name='Ngày Sinh (Người Khai Sinh)', blank=True, null=True)
    nksNgaySinhBangChu = models.CharField(
        max_length=100,  null=True, verbose_name='Ngày Sinh Bằng Chữ (Người Khai Sinh)', blank=True)
    nksNoiSinh = models.CharField(
        max_length=100,  null=True, verbose_name='Nơi Sinh Chi Tiết (Người Khai Sinh)', blank=True)
    nksNoiSinhDVHC = models.CharField(
        max_length=50,  null=True, verbose_name='Nơi Sinh Bằng Địa Vị Hành Chính (Người Khai Sinh)', blank=True)
    nksQueQuan = models.CharField(
        max_length=100,  null=True, verbose_name='Quê Quán (Người Khai Sinh)', blank=True)
    nksDanToc = models.CharField(max_length=26, choices=Options._DANTOC_LIST,
                                 verbose_name='Dân Tộc (Người Khai Sinh)', blank=True, default='Khác')
    nksQuocTich = models.CharField(max_length=65, choices=Options._COUNTRIES_LIST,
                                   default='Không có thông tin', verbose_name='Quốc Tịch (Người Khai Sinh)', blank=True)
    nksQuocTichKhac = models.CharField(
        max_length=65,  null=True, verbose_name='Quốc Tịch Khác (Người Khai Sinh)', blank=True)
    nksLoaiKhaiSinh = models.CharField(max_length=1,  null=True, verbose_name='Loại Khai Sinh (Người Khai Sinh)',
                                       choices=Options._BIRTH_CERT_TYPE, blank=False)

    # Thông tin mất tích của người khai sinh (5 trường)
    nksMatTich = models.CharField(
        max_length=10,  null=True, verbose_name='Mất Tích (Người Khai Sinh)', blank=True)
    nksMatTichNgayGhiChuTuyenBo = models.DateField(
        null=True, verbose_name='Ngày Ghi Chú Tuyên Bố Mất Tích (Người Khai Sinh)', blank=True)
    nksMatTichCanCuTuyenBo = models.CharField(
        max_length=10,  null=True, verbose_name='Căn Cứ Tuyên Bố Mất Tích (Người Khai Sinh)', blank=True)
    nksMatTichNgayGhiChuHuyTuyenBo = models.DateField(
        null=True, verbose_name='Ngày Ghi Chú Hủy Tuyên Bố Mất Tích (Người Khai Sinh)', blank=True)
    nksMatTichCanCuHuyTuyenBo = models.CharField(
        max_length=10,  null=True, verbose_name='Căn Cứ Hủy Tuyên Bố Mất Tích (Người Khai Sinh)', blank=True)

    # Thông tin hạn chế năng lực hành vi của người khai sinh (5 trường)
    nksHanCheNangLucHanhVi = models.CharField(
        max_length=10,  null=True, verbose_name='Hạn Chế Năng Lực Hành Vi (Người Khai Sinh)', blank=True)
    nksHanCheNangLucHanhViNgayGhiChuTuyenBo = models.DateField(
        max_length=10,  null=True, verbose_name='Ngày Ghi Chú Tuyên Bố Hạn Chế Năng Lực Hành Vi (Người Khai Sinh)', blank=True)
    nksHanCheNangLucHanhViCanCuTuyenBo = models.CharField(
        max_length=10,  null=True, verbose_name='Căn Cứ Tuyên Bố Hạn Chế Năng Lực Hành Vi (Người Khai Sinh)', blank=True)
    nksHanCheNangLucHanhViNgayGhiChuHuyTuyenBo = models.DateField(
        null=True, verbose_name='Ngày Ghi Chú Hủy Tuyên Bố Hạn Chế Năng Lực Hành Vi (Người Khai Sinh)', blank=True)
    nksHanCheNangLucHanhViNgayCanCuHuyTuyenBo = models.CharField(
        max_length=10,  null=True, verbose_name='Ngày Căn Cứ Hủy Tuyên Bố Hạn Chế Năng Lực Hành Vi (Người Khai Sinh)', blank=True)

    # Thông tin về mẹ của người khai sinh (9 trường)
    meHoTen = models.CharField(
        max_length=30,  null=True, verbose_name='Họ và Tên (Mẹ)', blank=True)
    meNgaySinh = models.DateField(
        null=True, verbose_name='Ngày Sinh (Mẹ)', blank=True)
    meDanToc = models.CharField(max_length=26, choices=Options._DANTOC_LIST,
                                null=True, verbose_name='Dân Tộc (Mẹ)', blank=True)
    meQuocTich = models.CharField(
        max_length=20,  null=True, verbose_name='Quốc Tịch (Mẹ)', blank=True)
    meQuocTichKhac = models.CharField(
        max_length=10,  null=True, verbose_name='Quốc Tịch Khác (Mẹ)', blank=True)
    meLoaiCuTru = models.CharField(max_length=1, choices=Options._RESIDENCE_TYPE,
                                   null=True, verbose_name='Loại Cư Trú (Mẹ)', blank=True)
    meNoiCuTru = models.CharField(
        max_length=100,  null=True, verbose_name='Nơi Cư Trú (Mẹ)', blank=True)
    meLoaiGiayToTuyThan = models.CharField(
        max_length=1, choices=Options._IDENTIFICATION_TYPE,  null=True, verbose_name='Loại Giấy Tờ Tùy Thân (Mẹ)', blank=True)
    meSoGiayToTuyThan = models.CharField(
        max_length=12,  null=True, verbose_name='Số Giấy Tờ Tùy Thân (Mẹ)', blank=True)

    # Thông tin về cha của người khai sinh (9 trường)
    chaHoTen = models.CharField(
        max_length=30,  null=True, verbose_name='Họ Tên (Cha)', blank=True)
    chaNgaySinh = models.DateField(
        null=True, verbose_name='Ngày Sinh (Cha)', blank=True)
    chaDanToc = models.CharField(max_length=26, choices=Options._DANTOC_LIST,
                                 null=True, verbose_name='Dân Tộc (Cha)', blank=True)
    chaQuocTich = models.CharField(
        max_length=20,  null=True, verbose_name='Quốc Tịch (Cha)', blank=True)
    chaQuocTichKhac = models.CharField(
        max_length=20,  null=True, verbose_name='Quốc Tịch Khác (Cha)', blank=True)
    chaLoaiCuTru = models.CharField(
        max_length=1,  null=True, verbose_name='Loại Cư Trú (Cha)', blank=True)
    chaNoiCuTru = models.CharField(
        max_length=100,  null=True, verbose_name='Nơi Cư Trú (Cha)', blank=True)
    chaLoaiGiayToTuyThan = models.CharField(
        max_length=1,  null=True, verbose_name='Loại Giấy Tờ Tùy Thân (Cha)', blank=True)
    chaSoGiayToTuyThan = models.CharField(
        max_length=12,  null=True, verbose_name='Số Giấy Tờ Tùy Thân (Cha)', blank=True)

    # Thông tin về người đi khai - người yêu cầu (7 trường)
    nycHoTen = models.CharField(
        max_length=30,  null=True, verbose_name='Họ Tên (Người Yêu Cầu)', blank=True)
    nycQuanHe = models.CharField(
        max_length=10,  null=True, verbose_name='Quan Hệ (Người Yêu Cầu)', blank=True)
    nycLoaiGiayToTuyThan = models.CharField(max_length=1, choices=Options._IDENTIFICATION_TYPE,
                                            null=True, verbose_name='Loại Giấy Tờ Tùy Thân (Người Yêu Cầu)', blank=True)
    nycGiayToKhac = models.CharField(
        max_length=20,  null=True, verbose_name='Giấy Tờ Khác (Người Yêu Cầu)', blank=True)
    nycSoGiayToTuyThan = models.CharField(
        max_length=12,  null=True, verbose_name='Số Giấy Tờ Tùy Thân (Người Yêu Cầu)', blank=True)
    nycNgayCapGiayToTuyThan = models.DateField(
        null=True, verbose_name='Ngày Cấp Giấy Tờ Tùy Thân (Người Yêu Cầu)', blank=True)
    nycNoiCapGiayToTuyThan = models.CharField(
        max_length=100,  null=True, verbose_name='Nơi Cấp Giấy Tờ Tùy Thân (Người Yêu Cầu)', blank=True)

    # Thông tin đăng ký nước ngoài (4 trường)
    soDangKyNuocNgoai = models.CharField(
        max_length=12,  null=True, verbose_name="Số Đăng Ký Nước Ngoài", blank=True)
    ngayDangKyNuocNgoai = models.DateField(
        null=True, verbose_name="Ngày Đăng Ký Nước Ngoài", blank=True)
    cqNuocNgoaiDaDangKy = models.CharField(
        max_length=30,  null=True, verbose_name="Cơ Quan Đăng Ký Nước Ngoài", blank=True)
    qgNuocNgoaiDaDangKy = models.CharField(
        max_length=63, choices=Options._COUNTRIES_LIST,  null=True, verbose_name="Quốc Gia Đăng Ký Nước Ngoài", blank=True)

    def __str__(self):
        return self.document.document_name


class Marriage_Status_Document(models.Model):

    document = models.ForeignKey(
        Document, blank=True, null=True, on_delete=models.CASCADE)
    executor = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.SET_NULL)

    so = models.CharField(max_length=10, default='',
                          verbose_name='Số', blank=True)
    quyenSo = models.CharField(
        max_length=10, default='', verbose_name='Quyển Số', blank=True)
    trangSo = models.CharField(
        max_length=10, default='', verbose_name='Trang Số', blank=True)
    ngayDangKy = models.DateField(
        verbose_name='Ngày Đăng Ký', blank=True)
    noiCap = models.CharField(
        max_length=40, default='', verbose_name='Nơi Cấp', blank=True)
    nguoiKy = models.CharField(
        max_length=20, default='', verbose_name='Người Ký', blank=True)
    chucVuNguoiKy = models.CharField(
        max_length=15, default='', verbose_name='Chức Vụ Người Ký', blank=True)
    nguoiThucHien = models.CharField(
        max_length=40, default='', verbose_name='Người Thực Hiện', blank=True)
    ghiChu = models.CharField(
        max_length=10, default='', verbose_name='Ghi Chú', blank=True)

    nxnHoTen = models.CharField(
        max_length=30, default='', verbose_name='nxn_Họ Tên', blank=True)
    nxnGioiTinh = models.CharField(
        max_length=1, choices=Options._SEX_TYPE, default='3', verbose_name='nxn_Giới Tính', blank=True)
    nxnNgaySinh = models.DateField(
        verbose_name='nxn_Ngày Sinh', blank=True, null=True)
    nxnDanToc = models.CharField(max_length=26, choices=Options._DANTOC_LIST,
                                 default='', verbose_name='nxn_Dân Tộc', blank=True)
    nxnQuocTich = models.CharField(max_length=65, choices=Options._COUNTRIES_LIST,
                                   default='Không có thông tin', verbose_name='nxn_Quốc Tịch', blank=True)
    nxnQuocTichKhac = models.CharField(
        max_length=20, default='', verbose_name='nxn_Quốc Tịch Khác', blank=True)
    nxnLoaiCuTru = models.CharField(max_length=1, choices=Options._RESIDENCE_TYPE,
                                    default='0', verbose_name='nxn_Loại Cư Trú', blank=True)
    nxnNoiCuTru = models.CharField(
        max_length=40, default='', verbose_name='nxn_Nơi Cư Trú', blank=True)
    nxnLoaiGiayToTuyThan = models.CharField(
        max_length=1, choices=Options._IDENTIFICATION_TYPE, default='0', verbose_name='nxn_Loại Giấy Tờ Tùy Thân', blank=True)
    nxnGiayToKhac = models.CharField(
        max_length=20, default='', verbose_name='nxn_Giấy Tờ Khác', blank=True)
    nxnSoGiayToTuyThan = models.CharField(
        max_length=1, default='', verbose_name='nxn_Số Giấy Tờ Tùy Thân', blank=True)
    nxnNgayCapGiayToTuyThan = models.DateField(
        verbose_name='nxn_Ngày Cấp Giấy Tờ Tùy Thân', blank=True, null=True)
    nxnNoiCapGiayToTuyThan = models.CharField(
        max_length=30, default='', verbose_name='nxn_Nơi Cấp Giấy Tờ Tùy Thân', blank=True)
    nxnThoiGianCuTruTai = models.CharField(
        max_length=15, default='', verbose_name='nxn_Thời Gian Cư Trú Tại', blank=True)
    nxnThoiGianCuTruTu = models.CharField(
        max_length=12, default='', verbose_name='nxn_Thời Gian Cư Trú Từ', blank=True)
    nxnThoiGianCuTruDen = models.CharField(
        max_length=12, default='', verbose_name='nxn_Thời Gian Cư Trú Đến', blank=True)
    nxnTinhTrangHonNhan = models.CharField(
        max_length=30, default='', verbose_name='nxn_Tình Trạng HÔn Nhân', blank=True)
    nxnLoaiMucDiSuDung = models.CharField(
        max_length=30, choices=Options._INTENDED_USE, default='1', verbose_name='nxn_Loại Mục Đích Sử Dụng', blank=True)
    nxnMucDiSuDung = models.CharField(
        max_length=30, default='', verbose_name='nxn_Mục Đích Sử Dụng', blank=True)

    nycHoTen = models.CharField(
        max_length=30, default='', verbose_name='nyc_Họ Tên', blank=True)
    nycQuanHe = models.CharField(
        max_length=10, default='', verbose_name='nyc_Quan Hệ', blank=True)
    nycLoaiGiayToTuyThan = models.CharField(
        max_length=10, choices=Options._IDENTIFICATION_TYPE, default='0', verbose_name='nyc_Loại Giấy Tờ Tùy Thân', blank=True)
    nycGiayToKhac = models.CharField(
        max_length=10, default='', verbose_name='nyc_Giấy Tờ Khác', blank=True)
    nycSoGiayToTuyThan = models.CharField(
        max_length=12, default='', verbose_name='nyc_Số Giấy Tờ Tùy Thân', blank=True)
    nycNgayCapGiayToTuyThan = models.DateField(
        verbose_name='nyc_Ngày Cấp Giấy Tờ Tùy Thân', blank=True, null=True)
    nycNoiCapGiayToTuyThan = models.CharField(
        max_length=15, default='', verbose_name='nyc_Nơi Cấp Giấy Tờ Tùy Thân', blank=True)

    def __str__(self):
        return self.document.document_name


class Marriage_Certificate_Document(models.Model):

    document = models.ForeignKey(
        Document, blank=True, null=True, on_delete=models.CASCADE)
    executor = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.SET_NULL)

    so = models.CharField(max_length=10, default='',
                          verbose_name='Số', blank=True)
    trangSo = models.CharField(
        max_length=10, default='', verbose_name='Trang Số', blank=True)
    ngayDangKy = models.DateField(
        verbose_name='Ngày Đăng Ký', blank=True)
    loaiDangKy = models.CharField(max_length=50, choices=Options._REGISTER_STATUS,
                                  default='1', verbose_name='Loại Đăng Ký', blank=True)
    nguoiKy = models.CharField(
        max_length=100, default=' ', verbose_name='Người Ký', blank=True)
    chucVuNguoiKy = models.CharField(
        max_length=100, default=' ', verbose_name='Chức vụ người ký', blank=True)
    nguoiThucHien = models.CharField(
        max_length=100, default='Công Chức Tư Pháp - Hộ Tịch', verbose_name='Người thực hiện', blank=True)
    ghiChu = models.CharField(max_length=500, default=' ', verbose_name='Ghi chú', blank=True)
    tinhTrangKetHon = models.CharField(
        max_length=50, choices=Options._MARRIED_STATUS, default='4', verbose_name='Tình trạng kết hôn', blank=True)

    chongHoTen = models.CharField(
        max_length=100, default=' ', verbose_name='Chồng_Họ tên', blank=True)
    chongNgaySinh = models.DateField(
        verbose_name='Chồng_Ngày sinh', blank=True, null=True)
    chongDanToc = models.CharField(max_length=30, choices=Options._DANTOC_LIST,
                                   default='', verbose_name='Chồng_Dân tộc', blank=True)
    chongQuocTich = models.CharField(max_length=63, choices=Options._COUNTRIES_LIST,
                                     default='', verbose_name='Chồng_Quốc tịch', blank=True)
    chongLoaiCuTru = models.CharField(
        max_length=30, choices=Options._RESIDENCE_TYPE, verbose_name='Chồng_Loại cư trú', blank=True)
    chongNoiCuTru = models.CharField(max_length=100, default=' ', verbose_name='Chồng_Nơi cư trú', blank=True)
    chongLoaiGiayToTuyThan = models.CharField(
        max_length=30, choices=Options._IDENTIFICATION_TYPE, default='9', verbose_name='Chồng_Loại giấy tờ tùy thân', blank=True)
    chongSoGiayToTuyThan = models.CharField(
        max_length=50, default=' ', verbose_name='Chồng_Số giấy tờ tùy thân', blank=True)
    chongNgayCapGiayToTuyThan = models.DateField(
        verbose_name='Chồng_Ngày cấp giấy tờ tùy thân', blank=True, null=True)
    chongNoiCapGiayToTuyThan = models.CharField(max_length=500, default=' ', verbose_name='Chồng_Nơi cấp giấy tờ tùy thân', blank=True)

    voHoTen = models.CharField(
        max_length=100, default=' ', verbose_name='Vợ_Họ tên', blank=True)
    voNgaySinh = models.DateField(
        verbose_name='Vợ_Ngày sinh', blank=True, null=True)
    voDanToc = models.CharField(max_length=100, choices=Options._DANTOC_LIST,
                                default='', verbose_name='Vợ_Dân tộc', blank=True)
    voQuocTich = models.CharField(max_length=100, choices=Options._COUNTRIES_LIST,
                                  default='', verbose_name='Vợ_Quốc tịch', blank=True)
    voQuocTichKhac = models.CharField(max_length=100, choices=Options._COUNTRIES_LIST,
                                      default='', verbose_name='Vợ_Quốc tịch khác', blank=True)
    voLoaiCuTru = models.CharField(
        max_length=30, choices=Options._RESIDENCE_TYPE, verbose_name='Vợ_Loại cư trú', blank=True)
    voNoiCuTru = models.CharField(max_length=500, default=' ', verbose_name='Vợ_Nơi cư trú', blank=True)
    voLoaiGiayToTuyThan = models.CharField(
        max_length=30, choices=Options._IDENTIFICATION_TYPE, default='9', verbose_name='Vợ_Loại giấy tờ tùy thân', blank=True)
    voSoGiayToTuyThan = models.CharField(
        max_length=50, default=' ', verbose_name='Vợ_Số giấy tờ tùy thân', blank=True)
    voNgayCapGiayToTuyThan =  models.DateField(
        verbose_name='Vợ_Ngày cấp giấy tờ tùy thân', blank=True, null=True)
    voNoiCapGiayToTuyThan = models.CharField(max_length=500, default=' ', verbose_name='Vợ_Nơi cấp giấy tờ tùy thân', blank=True)

    def __str__(self):
        return self.document.document_name
