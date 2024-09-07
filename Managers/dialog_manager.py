import pygame

class DialogManager:
    def __init__(self):
        # 使用支持中文的字体或指定系统默认字体
        self.font_path = "./assets/fonts/SourceHanSerifSC-VF.otf"
        self.font_size = 24
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.active = False
        self.dialogs = []
        self.current_dialog_index = 0
        self.text_surface = None

        # 初始化对话框位置和大小
        self.background_color = (0, 0, 0)
        self.text_color = (255, 255, 255)

    def show(self, dialogs):
        """接受一个对话列表"""
        self.active = True
        self.dialogs = dialogs
        self.current_dialog_index = 0
        self.update_text_surface()
        from game import Game
        player = Game.get_instance().view.player
        player.block_move = True

    def update_text_surface(self):
        """更新当前对话的文本显示"""
        if self.current_dialog_index < len(self.dialogs):
            text = self.dialogs[self.current_dialog_index]
            self.text_surface = self.font.render(text, True, self.text_color)
        else:
            self.hide()

    def hide(self):
        """隐藏对话框"""
        self.active = False
        self.dialogs = []
        self.current_dialog_index = 0
        self.text_surface = None
        from game import Game
        player = Game.get_instance().view.player
        player.block_move = False

    def next_dialog(self):
        """切换到下一段对话"""
        self.current_dialog_index += 1
        self.update_text_surface()

    def update(self):
        if not self.active:
            return

        from game import Game
        game_instance = Game.get_instance()

        # 监听用户按键（如空格、回车）或鼠标左键以切换对话
        get_next = False
        def get_next_dialog():
            nonlocal get_next
            get_next = True
        game_instance.keyboard_manager.first_down("Space", get_next_dialog)
        game_instance.keyboard_manager.first_down("Enter", get_next_dialog)
        game_instance.mouse_manager.first_down("Left", get_next_dialog)
        if get_next:
            self.next_dialog()

    def draw(self):
        if not self.active or not self.text_surface:
            return

        from game import Game
        screen = Game.get_instance().screen
        screen_width, screen_height = screen.get_size()

        # 对话框的固定位置和大小，放置在屏幕的下半部分
        dialog_width, dialog_height = 600, 150
        dialog_x = (screen_width - dialog_width) // 2
        dialog_y = screen_height - dialog_height - 20  # 屏幕底部上方20像素
        self.rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)

        # 绘制背景框
        Game.get_instance().draw_rect(self.background_color, self.rect)

        # 在对话框内水平和垂直居中绘制文本
        text_x = self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2
        screen.blit(self.text_surface, (text_x, text_y))
