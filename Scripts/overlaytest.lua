-- create an overlay the size of the current layer
local g = golly()
local ov = g.overlay
local viewwd, viewht = g.getview(g.getlayer())
ov("create "..viewwd.." "..viewht)
-- open example pattern
-- g.open(g.getdir("app").."Patterns/Life/Methuselahs/rabbits.lif")
-- create a cell view using a theme
ov("cellview -256 -256 512 512")
ov("celloption grid 1")
ov("celloption stars 1")
-- ov("theme 0 255 255 255 255 255 0 0 255 0 0 47 0 0 0")
-- set camera 14.5x zoom and 30 degree rotation
g.setoption("showicons", 1)
ov("camera zoom 16")
ov("camera angle 45")
ov("drawcells")
ov("update")
-- run for 1000 generations
for i = 1, 10 do
    g.run(1)
    ov("updatecells")
	ov("celloption grid 1")
    ov("drawcells")
    ov("update")
	    -- loop until key pressed or mouse clicked
	return_to_main_menu = false
    while not return_to_main_menu do
        local event = g.getevent()
        if event:find("^oclick") or event == "key space none" then
            -- return to main menu
            return_to_main_menu = true
        end
	end
end
-- delete the overlay
ov("delete") 