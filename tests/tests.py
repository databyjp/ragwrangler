# TODO

# # Test with slightly altered source texts
# alt_source_text = test_source_text.replace("the", "THE")
# alt_source_text2 = test_source_text[10:-10]
#
# for alt_text in [alt_source_text, alt_source_text2]:
#     output = quiz_rag.get_output(source_text=alt_text)
#     print(truncate_text(str(output), max_length=200))
#
# # Test with actually different source texts
# wrong_text = """
# Supersonic speed is the speed of an object that exceeds the speed of sound (Mach 1). For objects traveling in dry air of a temperature of 20 °C (68 °F) at sea level, this speed is approximately 343.2 m/s (1,126 ft/s; 768 mph; 667.1 kn; 1,236 km/h). Speeds greater than five times the speed of sound (Mach 5) are often referred to as hypersonic. Flights during which only some parts of the air surrounding an object, such as the ends of rotor blades, reach supersonic speeds are called transonic. This occurs typically somewhere between Mach 0.8 and Mach 1.2.
#
# Sounds are traveling vibrations in the form of pressure waves in an elastic medium. Objects move at supersonic speed when the objects move faster than the speed at which sound propagates through the medium. In gases, sound travels longitudinally at different speeds, mostly depending on the molecular mass and temperature of the gas, and pressure has little effect. Since air temperature and composition varies significantly with altitude, the speed of sound, and Mach numbers for a steadily moving object may change. In water at room temperature supersonic speed can be considered as any speed greater than 1,440 m/s (4,724 ft/s). In solids, sound waves can be polarized longitudinally or transversely and have even higher velocities.
#
# Supersonic fracture is crack motion faster than the speed of sound in a brittle material.
# """
#
# output = quiz_rag.get_output(source_text=wrong_text)
# print(truncate_text(str(output), max_length=200))
