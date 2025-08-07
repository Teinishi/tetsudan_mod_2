-- include sfx 0 "m_tns_tetsudan_controller_4.ogg"

function clamp(x, a, b)
	return math.min(math.max(x, a), b)
end

function lerp(a, b, t)
	return a*(1 - t) + b*t
end

local pos = nil
local theta = nil
local transform = matrix.identity()

function update()
	if not pos then return end
	local theta_tgt = -pos*45/180*math.pi
	theta = theta ~= nil and lerp(theta, theta_tgt, 0.4) or theta_tgt
	transform = matrix.rotationY(theta)
end

function onParse()
	pos, _ = parser.parseNumber("pos", pos)
	update()
end

function onTick()
	local value, success = component.getInputLogicSlotFloat(0)
	if success then
		local npos = clamp(math.floor(value + 0.5), -1, 1)
		if pos ~= nil and npos ~= pos then
			component.sfxPlayOnce(0, 0, 0, 0, 0, 1, 6, 1, 1, 0.5)
		end
		pos = npos
		update()
	end
end

function onRender()
	component.renderMesh0(transform)
end
