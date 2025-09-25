local sch = property.getNumber"Speed Ch."
local RUNNING_SOUND_INDICES = {}
for s in (property.getText"Running Sound"):gmatch("([^,]+)") do
	table.insert(RUNNING_SOUND_INDICES, tonumber(s))
end

function onTick()
	local speed = input.getNumber(sch)
	local volume = speed*3.6/60
	for _, i in ipairs(RUNNING_SOUND_INDICES) do
		output.setNumber(2*i - 1, volume)
		output.setNumber(2*i, speed)
	end
end
