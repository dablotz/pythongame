""" Draw a stick figure. """

import pygame

def draw_stick_figure(screen, rect, color=(0, 0, 0)):
    """ Draw a stick figure at the given rectangle position. """
    # Head
    head_radius = rect.width // 4
    head_center = (rect.centerx, rect.top + head_radius)
    pygame.draw.circle(screen, color, head_center, head_radius, 2)

    # Body line
    body_start = (rect.centerx, rect.top + 2 * head_radius)
    body_end = (rect.centerx, rect.bottom - rect.height // 4)
    pygame.draw.line(screen, color, body_start, body_end, 2)

    # Arms
    arm_y = rect.top + rect.height // 2
    pygame.draw.line(screen, color, (rect.left + 5, arm_y), (rect.right - 5, arm_y), 2)

    # Legs
    leg_start = body_end
    left_leg_end = (rect.left + 10, rect.bottom)
    right_leg_end = (rect.right - 10, rect.bottom)
    pygame.draw.line(screen, color, leg_start, left_leg_end, 2)
    pygame.draw.line(screen, color, leg_start, right_leg_end, 2)
