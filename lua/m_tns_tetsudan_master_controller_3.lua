-- include sfx 0 "m_tns_tetsudan_controller_4.ogg"

function clamp(x, a, b)
	return math.min(math.max(x, a), b)
end

function lerp(a, b, t)
	return a*(1 - t) + b*t
end

function invlerp(v, a, b)
	if a == b then
		return 0
	end
	return (v - a) / (b - a)
end

function sel(b, t, f)
	if b then
		return t
	else
		return f
	end
end

local DEFAULT_POS_A, DEFAULT_POS_B = -5, 5
local DEFAULT_THETA_A, DEFAULT_THETA_B = -130/180*math.pi, 130/180*math.pi

local pos_a, pos_b = DEFAULT_POS_A, DEFAULT_POS_B
local theta_a, theta_b = DEFAULT_THETA_A, DEFAULT_THETA_B
local pos = nil
local theta = nil
local btn_press = 0
local transform0, transform1 = matrix.identity(), matrix.identity()

function update()
	if not pos then return end
	local theta_tgt = lerp(theta_a, theta_b, invlerp(pos, pos_a, pos_b))
	if theta == theta_tgt then return end
	theta = theta ~= nil and lerp(theta, theta_tgt, 0.4) or theta_tgt
	btn_press = lerp(btn_press, pos ~= 0 and 1 or 0, 0.7)
	transform0 = matrix.rotationY(theta)
	transform1 = matrix.multiply(transform0, matrix.translation(0, 0, 0.012*btn_press))
end

function onParse()
	pos, _ = parser.parseNumber("pos", pos)
	update()
end

function onTick()
	local composite, success = component.getInputLogicSlotComposite(0)
	if success then
		local fv = composite.float_values

		local pos_range = fv[1] ~= 0 or fv[2] ~= 0
		pos_a = sel(pos_range, math.floor(fv[1] + 0.5), DEFAULT_POS_A)
		pos_b = sel(pos_range, math.floor(fv[2] + 0.5), DEFAULT_POS_B)

		theta_range = fv[3] ~= 0 or fv[4] ~= 0
		theta_a = sel(theta_range, fv[3], DEFAULT_THETA_A)
		theta_b = sel(theta_range, fv[4], DEFAULT_THETA_B)
	end

	local value, success = component.getInputLogicSlotFloat(0)
	if success then
		local npos = clamp(math.floor(value + 0.5), pos_a, pos_b)
		if pos ~= nil and npos ~= pos then
			component.sfxPlayOnce(0, 0, 0, 0, 0, 1, 6, 1, 1.2, 0.5)
		end
		pos = npos
		update()
	end
end

function onRender()
	component.renderMesh0(transform0)
	component.renderMesh1(transform1)
end
