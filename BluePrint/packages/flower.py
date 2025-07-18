from flask import Blueprint, render_template

flower=Blueprint("flower",__name__,static_folder="",template_folder="")
#this above variable flower is the blueprint and package file name is flower and to make this folder as package 
#we have __init__.py
@flower.route("/")
@flower.route("/home")
def flower1():
    return "Imported this file"