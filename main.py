import kivy
kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
import random

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
            #ball.r -= 0.1
            ball.g -= 0.1
            ball.b -= 0.15
            if(ball.center_y > self.center_y - 50 and ball.center_y < self.center_y + 50):
                self.height += 10
                self.y -= 5

    def resetPaddle(self):
            self.y = self.center_y - 100
            self.height = 200
            


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    r = NumericProperty(1)
    g = NumericProperty(1)
    b = NumericProperty(1)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
    
    def resetColor(self):            
            self.g = 1
            self.b = 1

class PongGame(Widget):
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    ball3 = ObjectProperty(None)
    ball4 = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    allball = ReferenceListProperty(ball1,ball2,ball3,ball4)
    
    def serve_ball(self, ball, vel=(4, 0)):
        ball.center = self.center
        ball.velocity = vel

    def update(self, dt):
        for ball in self.allball:
            ball.move()

        #bounce ball off paddles
            self.player1.bounce_ball(ball)
            self.player2.bounce_ball(ball)
        
        #bounce ball off bottom or top
            if (ball.y < self.y) or (ball.top > self.top):
                ball.velocity_y *= -1
            

        #went off a side to score point?
            if ball.center_x < self.x:
                self.player2.score += 1
                self.player1.resetPaddle()
                ball.resetColor()
                self.serve_ball(ball,vel=(4, random.uniform(-1,1)))
                
            if ball.center_x > self.width:
                self.player1.score += 1
                self.player2.resetPaddle()
                ball.resetColor()
                self.serve_ball(ball,vel=(-4, random.uniform(-1,1)))
        
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball(game.allball[0],vel=(4,1))
        game.serve_ball(game.allball[1],vel=(-4,1))
        game.serve_ball(game.allball[2],vel=(4,-1))
        game.serve_ball(game.allball[3],vel=(-4,-1))

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
