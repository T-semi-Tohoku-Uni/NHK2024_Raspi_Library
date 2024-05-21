from enum import Enum
from typing import Callable

class OneStateButton(Enum):
    WAIT = 0x00
    FINISH = 0x01

class OneStateButtonHandler:
    def __init__(self, state=OneStateButton.WAIT):
        self.state = state
    
    def handle_button(
        self,
        is_pressed: int,
        action_send: Callable[[], None]
    ):
        if is_pressed and self.state == OneStateButton.WAIT:
            self.state = OneStateButton.FINISH
            action_send()
            
        if not is_pressed and self.state == OneStateButton.FINISH:
            self.state = OneStateButton.WAIT

class TwoStateButton(Enum):
    WAIAT_0 = 0x00
    FINISH_0 = 0x01
    WAIT_1 = 0x10
    FINISH_1 = 0x11
    
class TwoStateButtonHandler:
    def __init__(self, state=TwoStateButton.WAIAT_0):
        self.state = state
    
    def handle_button(
        self, 
        is_pressed: int, 
        action_send_0: Callable[[], None], 
        action_send_1: Callable[[], None]
    ):
        
        if is_pressed and self.state == TwoStateButton.WAIAT_0:
            self.state = TwoStateButton.FINISH_0
            action_send_0()
        
        if not is_pressed and self.state == TwoStateButton.FINISH_0:
            self.state = TwoStateButton.WAIT_1
        
        if is_pressed and self.state == TwoStateButton.WAIT_1:
            self.state = TwoStateButton.FINISH_1
            action_send_1()
        
        if not is_pressed and self.state == TwoStateButton.FINISH_1:
            self.state = TwoStateButton.WAIAT_0
    
    def transision_next_state(
        self,
        current_state: int,
    ):
        if current_state == 0:
            self.state = TwoStateButton.WAIT_1
        elif current_state == 1:
            self.state = TwoStateButton.WAIAT_0
         
class ThreeStateButton(Enum):
    WAIT_0 = 0x00
    FINISH_0 = 0x01
    WAIT_1 = 0x10
    FINISH_1 = 0x11
    WAIT_2 = 0x20
    FINISH_2 = 0x21
    
class ThreeStateButtonHandler:
    def __init__(self, state=ThreeStateButton.WAIT_0):
        self.state = state
    
    def handle_button(
        self, 
        is_pressed: int, 
        action_send_0: Callable[[], None], 
        action_send_1: Callable[[], None],
        action_send_2: Callable[[], None]
    ):
        if is_pressed and self.state == ThreeStateButton.WAIT_0:
            self.state = ThreeStateButton.FINISH_0
            action_send_0()
        
        if not is_pressed and self.state == ThreeStateButton.FINISH_0:
            self.state = ThreeStateButton.WAIT_1
        
        if is_pressed and self.state == ThreeStateButton.WAIT_1:
            self.state = ThreeStateButton.FINISH_1
            action_send_1()
        
        if not is_pressed and self.state == ThreeStateButton.FINISH_1:
            self.state = ThreeStateButton.WAIT_2
        
        if is_pressed and self.state == ThreeStateButton.WAIT_2:
            self.state = ThreeStateButton.FINISH_2
            action_send_2()
        
        if not is_pressed and self.state == ThreeStateButton.FINISH_2:
            self.state = ThreeStateButton.WAIT_0
        
    